# LXML library is faster for writing purposes
from lxml import etree
import datetime
import collections

class PMML_Exporter:
    """
    PMML file format exporter used to visualize association rules in R
    """
    def __init__(self, min_sup = 0.0, min_conf = 0.0, transaction_num = 0, uniques = None, freq_itemsets = None, arules = None):
        """
        Necessary fields to export association rules into PMML format
        :param min_sup: Minimum support (int)
        :param min_conf: Minimum confidence (int)
        :param transaction_num: Number of transactions (int)
        :param uniques: Unique itemsets (dict)
        :param freq_itemsets:
        :param arules:
        """
        print("This will be exporter class that has a static function to export our data")
        # Check inputs
        if uniques is None or freq_itemsets is None or arules is None:
            raise('None of the inputs cannot be None')
        # Global attiributes
        self.transaction_number = transaction_num
        self.uniques_with_id = self._numerate_uniques(uniques) # Could be refactored to 1 line
        self.arules = arules
        self.freq_itemsets = freq_itemsets
        self.min_sup = min_sup
        self.min_conf = min_conf

    def export(self, path = 'pmml.xml'):
        """
        Exports the association rules into PMML format
        :param path: File location to be saved (str)
        :return:
        """
        print('PMML file export - initiated')
        root = self._write_root()
        root.append(self._write_header())
        root.append(self._write_dd())
        print('PMML file export - Write association models')
        root.append(self._write_assoc_model())
        xml = etree.tostring(root, xml_declaration=True, pretty_print=True, encoding='UTF-8')
        # Save the file
        self._save_xml(xml, path)

    def _save_xml(self, xml, path):
        """
        Saves the xml file into specified location
        :param xml: Xml root (etree)
        :param path: File location to be saved (str)
        :return:
        """
        print('Association model is exported successfully')
        with open(path, 'wb') as f:
                f.write(xml)


    def _write_assoc_model(self):
        """ Main association model lxml writer """
        assoc_model = etree.Element("AssociationModel",
                                    functionName="associationRules",
                                    numberOfTransactions = str(self.transaction_number),
                                    numberOfItems = str(len(self.uniques_with_id)),
                                    minimumSupport = str(self.min_sup),
                                    minimumConfidence = str(self.min_conf),
                                    numberOfItemsets = str(len(self.freq_itemsets)),
                                    numberOfRules=str(len(self.arules)))
        mining_schema = etree.Element("MiningSchema")
        mf1 = etree.Element("MiningField", name="transaction", usageType="group")
        mf2 = etree.Element("MiningField", name="item", usageType="active")
        mining_schema.append(mf1)
        mining_schema.append(mf2)
        assoc_model.append(mining_schema)
        # Add unique items to assoc_model
        assoc_model = self._write_items(assoc_model)
        assoc_model = self._write_itemsets(assoc_model)
        assoc_model = self._write_arules(assoc_model)
        return assoc_model
    
    def _write_dd(self):
        """ DataDictionary lxml writer """
        # This is required for specifiying PMML format
        df1 = etree.Element("DataField", name = "transaction", optype="categorical", dataType="string")
        df2 = etree.Element("DataField", name = "item", optype="categorical", dataType="string")
        dd = etree.Element("DataDictionary", numberOfFields = "2")
        dd.append(df1)
        dd.append(df2)
        return dd
    
    def _write_header(self):
        """ XML header writer """
        extension = etree.Element("Extension", name="user", value="eozer", extender="Rattle/PMML")
        application = etree.Element("Application", name="Rattle/PMML", version="1.4")
        timestamp = etree.Element("Timestamp")
        time = str('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
        timestamp.text = time
        header = etree.Element("Header", copyright = "Copyright (c) 2017 eozer", description="arules association rules model")
        header.append(extension)
        header.append(application)
        header.append(timestamp)
        
        return header
    
    def _write_root(self):
        """ Root element lxml writer """
        xmlns = "http://www.dmg.org/PMML-4_3"
        xsi = "http://www.w3.org/2001/XMLSchema-instance"
        schemaLocation = "http://www.dmg.org/PMML-4_3 http://www.dmg.org/pmml/v4-3/pmml-4-3.xsd"
        version = "4.3"
        ns = "{xsi}"
        # Generate root element
        root = etree.Element("{" + xmlns + "}PMML",
                             version = version,
                             attrib = {"{" + xsi + "}schemaLocation" : schemaLocation},
                             nsmap = {'xsi': xsi, None: xmlns})
        return root

    def _numerate_uniques(self, uniques):
        """
        Converts uniques field to key: ID - value: FIELD dictionary format
        :param uniques: Uniques field (dict)
        :return: key:id, value:field (dict)
        """
        id = 0
        uid = collections.OrderedDict()
        for k in uniques.keys():
            id += 1
            uid[k] = id
        uid = collections.OrderedDict(sorted(uid.items(), key = lambda _: _[0]))
        return uid

    def _find_ref_items(self, item):
        """
        Finds the reference item number
        :param item: Item (str)
        :return: Id of the items
        """
        return self.uniques_with_id[item]

    def _find_ref_itemsets(self, itemsets):
        """
        Finds the reference itemsets
        :param itemsets: Itemsets (list)
        :return: Id of the itemsets
        """
        for _ in self.freq_itemsets:
            a = list()
            b = list()
            if isinstance(itemsets, str):
                a.append(str)
            else:
                a = itemsets
            # Fix for 1-length freq itemset, which is string
            if isinstance(_['ITEMS'], str):
                b.append(_['ITEMS'])
            else:
                b = _['ITEMS']
            if a == b:
                return _['ID']

    def _write_items(self, am):
        """
        LXML writer for items
        :param am: Association models root (etree)
        :return: Updated association model root (etree)
        """
        ui = self.uniques_with_id
        # Iterate over all unique_items and append the item to assoc_model
        for k in ui.keys():
            item = etree.Element("Item", id = str(ui[k]), value = str(k))
            am.append(item)
        return am

    def _write_itemsets(self, am):
        """
        LXML writer for itemsets
        :param am: Association models root (etree)
        :return: Updated association model root (etree)
        """
        # List of dicts - [{'ID': 1, 'FREQ': 5, 'ITEMS': ['RACE_IS_WHITE', 'SEX_IS_MALE']} ...
        fis = self.freq_itemsets
        # Go all over the list
        for fis in self.freq_itemsets:
            itemset_id = str(fis['ID'])
            if isinstance(fis['ITEMS'], str):
                numberofitems = 1
            else:
                numberofitems = len(fis['ITEMS'])
            # Create itemset xml element
            itemset = etree.Element("Itemset", id = itemset_id, numberOfItems = str(numberofitems))
            if isinstance(fis['ITEMS'], str):
                uid = str(self._find_ref_items(fis['ITEMS']))
                itemref = etree.Element("ItemRef", itemRef=uid)
                itemset.append(itemref)
            else:
                for i in range(numberofitems):
                    uid = str(self._find_ref_items(fis['ITEMS'][i]))
                    itemref = etree.Element("ItemRef", itemRef = uid)
                    itemset.append(itemref)
            # Append it to association model
            am.append(itemset)
        return am

    def _write_arules(self, am):
        """
        LXML writer for association rules
        :param am: Association models root (etree)
        :return: Updated association model root (etree)
        """
        for r in self.arules:
            sup = str(r['SUP'])
            conf = str(r['CONF'])
            lift = str(r['LIFT'])
            # Get the id of the itemsets
            left = str(self._find_ref_itemsets(r['LEFT']))
            right = str(self._find_ref_itemsets(r['RIGHT']))
            rule = etree.Element("AssociationRule",
                                 support = sup,
                                 confidence = conf,
                                 lift = lift,
                                 antecedent = left,
                                 consequent = right)
            am.append(rule)
        return am