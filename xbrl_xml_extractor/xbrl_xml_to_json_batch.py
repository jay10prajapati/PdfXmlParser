"""
parse_xbrl_from_xml_string_v2.py

This script 
    - batch-processes all XBRL XML files in the XBRL_XML directory, 
    - parses them, 
    - and converts their contents into structured JSON files in the XBRL_XML_JSON directory. 
It uses ElementTree for XML parsing and handles XBRL-specific namespaces and context linking. 
The script logs its progress and errors for easier debugging and traceability.
"""

import os
import sys
import xml.etree.ElementTree as ET
import json
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Define namespaces to properly parse XML elements. These are collected from the full XML file.
namespaces = {
    'xbrli': 'http://www.xbrl.org/2003/instance',
    'xbrldi': 'http://xbrl.org/2006/xbrldi',
    'ind-as': 'http://www.icai.org/xbrl/taxonomy/2017-03-31/ind-as',
    'in-ca': 'http://www.icai.org/xbrl/taxonomy/2017-03-31/in-ca',
    'link': 'http://www.xbrl.org/2003/linkbase',
    # Additional namespaces that might appear in the full document:
    'ind-as-roles': 'http://www.icai.org/xbrl/taxonomy/2017-03-31/ind-as-roles',
    'xl': 'http://www.xbrl.org/2003/XLink',
    'xs': 'http://www.w3.org/2001/XMLSchema',
    'net': 'http://www.xbrl.org/2009/role/net',
    'xbrldt': 'http://xbrl.org/2005/xbrldt',
    'in-ca-types': 'http://www.icai.org/xbrl/taxonomy/2017-03-31/in-ca-types',
    'ref': 'http://www.xbrl.org/2006/ref',
    'num': 'http://www.xbrl.org/dtr/type/numeric',
    'nonnum': 'http://www.xbrl.org/dtr/type/non-numeric',
    'in-ci-ent': 'http://www.icai.org/xbrl/taxonomy/2017-03-31/in-ca/in-ci-ent',
    'in-ca-roles': 'http://www.icai.org/xbrl/taxonomy/2017-03-31/in-ca-roles',
    'xsd': 'http://www.w3.org/2001/XMLSchema',
    'xlink': 'http://www.w3.org/1999/xlink',
    'negated': 'http://www.xbrl.org/2009/role/negated',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'iso4217': 'http://www.xbrl.org/2003/iso4217'
}


def parse_xbrl_to_json(xml_string):
    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError as e:
        return json.dumps({"error": f"Failed to parse XML: {e}"}, indent=4)

    contexts = {}
    data_elements = []

    # 1. Parse Contexts
    for context_elem in root.findall('xbrli:context', namespaces):
        context_id = context_elem.get('id')
        context_info = {
            "id": context_id,
            "entity": {},
            "period": {},
            "scenario": []
        }

        identifier_elem = context_elem.find('xbrli:entity/xbrli:identifier', namespaces)
        if identifier_elem is not None:
            context_info["entity"] = {
                "scheme": identifier_elem.get('scheme'),
                "value": identifier_elem.text.strip() if identifier_elem.text else ""
            }

        period_elem = context_elem.find('xbrli:period', namespaces)
        if period_elem is not None:
            start_date_elem = period_elem.find('xbrli:startDate', namespaces)
            end_date_elem = period_elem.find('xbrli:endDate', namespaces)
            instant_elem = period_elem.find('xbrli:instant', namespaces)

            if start_date_elem is not None and end_date_elem is not None:
                context_info["period"] = {
                    "type": "duration",
                    "startDate": start_date_elem.text.strip() if start_date_elem.text else "",
                    "endDate": end_date_elem.text.strip() if end_date_elem.text else ""
                }
            elif instant_elem is not None:
                context_info["period"] = {
                    "type": "instant",
                    "instant": instant_elem.text.strip() if instant_elem.text else ""
                }

        scenario_elem = context_elem.find('xbrli:scenario', namespaces)
        if scenario_elem is not None:
            for typed_member_elem in scenario_elem.findall('xbrldi:typedMember', namespaces):
                dimension_full = typed_member_elem.get('dimension')
                dimension = str(ET.QName(dimension_full)) if dimension_full else None
                domain_elem = next(iter(typed_member_elem), None)
                if domain_elem is not None:
                    domain_value_full = domain_elem.text.strip() if domain_elem.text else ""
                    domain_value = domain_value_full.split(':')[-1] if ':' in domain_value_full else domain_value_full
                    context_info["scenario"].append({
                        "type": "typedMember",
                        "dimension": dimension,
                        "value": domain_value
                    })
            for explicit_member_elem in scenario_elem.findall('xbrldi:explicitMember', namespaces):
                dimension_full = explicit_member_elem.get('dimension')
                dimension = str(ET.QName(dimension_full)) if dimension_full else None
                member_value_full_text = explicit_member_elem.text.strip() if explicit_member_elem.text else ""
                member_value = member_value_full_text.split(':')[-1] if ':' in member_value_full_text else member_value_full_text
                context_info["scenario"].append({
                    "type": "explicitMember",
                    "dimension": dimension,
                    "value": member_value
                })
        contexts[context_id] = context_info

    # 2. Parse Data Elements (Facts) and link to Contexts
    for elem in root.iter():
        context_ref = elem.get('contextRef')
        if context_ref:
            tag_name_full = elem.tag
            [uri, element] = tag_name_full[1:].split('}')  if tag_name_full.startswith('{') and '}' in tag_name_full else [tag_name_full, tag_name_full]
            element_name = str(ET.QName(element))
            namespace_uri = str(ET.QName(uri))
            namespace_prefix = ""
            for prefix, uri in namespaces.items():
                if uri == namespace_uri:
                    namespace_prefix = prefix
                    break
            value_raw = elem.text if elem.text else ""
            value = re.sub(r'<[^>]+>', '', value_raw).strip()
            unit_ref = elem.get('unitRef')
            decimals = elem.get('decimals')
            data_entry = {
                "elementName": element_name,
                "namespacePrefix": namespace_prefix,
                "namespaceURI": namespace_uri,
                "value": value,
                "contextRef": context_ref,
                "unitRef": unit_ref,
                "decimals": decimals,
                "contextDetails": contexts.get(context_ref)
            }
            data_elements.append(data_entry)
    return json.dumps(data_elements, indent=4)


def main():
    project_root = os.path.dirname(os.path.dirname(__file__))
    xbrl_xml_folder = os.path.join(project_root, "XBRL_XML")
    xbrl_json_folder = os.path.join(project_root, "XBRL_XML_JSON")
    os.makedirs(xbrl_json_folder, exist_ok=True)

    xml_files = [f for f in os.listdir(xbrl_xml_folder) if f.lower().endswith('.xml')]
    if not xml_files:
        logging.info(f"No XML files found in {xbrl_xml_folder}")
        return

    logging.info(f"Found {len(xml_files)} XML file(s) in {xbrl_xml_folder}")
    for xml_file in xml_files:
        xml_path = os.path.join(xbrl_xml_folder, xml_file)
        json_file = os.path.splitext(xml_file)[0] + ".json"
        json_path = os.path.join(xbrl_json_folder, json_file)
        logging.info(f"Processing {xml_file} ...")
        try:
            with open(xml_path, 'r', encoding='utf-8') as f:
                xml_content = f.read()
            json_output = parse_xbrl_to_json(xml_content)
            with open(json_path, 'w', encoding='utf-8') as jf:
                jf.write(json_output)
            logging.info(f"Saved JSON to {json_path}")
        except Exception as e:
            logging.error(f"Failed to process {xml_file}: {e}")

if __name__ == "__main__":
    logging.info("Starting XBRL XML to JSON batch conversion script...")
    main()
