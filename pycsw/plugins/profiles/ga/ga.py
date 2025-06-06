# -*- coding: utf-8 -*-
# =================================================================
#
# Author: Nicholas Car <nick@kurrawong.ai>
#
# Copyright (c) 2025 KurrawongAI
#
# This profile builds on the iso19115p3 profile supplied with pyCSW
# v3 by Vincent Fazio (CSIRO)
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import os
import json
from xml.etree.ElementTree import Element

from pycsw.core import config, util
from pycsw.core.etree import etree
from pycsw.plugins.profiles import profile
from datetime import datetime

CODELIST = 'codeListLocation'


# CHANGE - added
# MD_TopicCategoryCode
TOPIC_CATEGORY_CODES = {
    "farming": "farming",
    "biota": "biota",
    "boundaries": "boundaries",
    "climatologyMeteorologyAtmosphere": "climatologyMeteorologyAtmosphere",
    "economy": "economy",
    "elevation": "elevation",
    "environment": "environment",
    "geoscientificInformation": "geoscientificInformation",
    "health": "health",
    "imageryBaseMapsEarthCover": "imageryBaseMapsEarthCover",
    "intelligenceMilitary": "intelligenceMilitary",
    "inlandWaters": "inlandWaters",
    "location": "location",
    "oceans": "oceans",
    "planningCadastre": "planningCadastre",
    "society": "society",
    "structure": "structure",
    "transportation": "transportation",
    "utilitiesCommunication": "utilitiesCommunication",
    "extraTerrestrial": "extraTerrestrial",
    "disaster": "disaster",
}


class GA(profile.Profile):
    """ GaProfile class represents the profile for input and output of ISO 19115 Part 3 XML
    """
    def __init__(self, model, namespaces, context):
        """
        :param model: model
        :param namespaces: namespaces
        :param context: context
        """
        self.context = context

        self.namespaces = {
            "mdb":"http://standards.iso.org/iso/19115/-3/mdb/1.0",
            "cat":"http://standards.iso.org/iso/19115/-3/cat/1.0",
            "gfc":"http://standards.iso.org/iso/19110/gfc/1.1",
            "cit":"http://standards.iso.org/iso/19115/-3/cit/1.0",
            "gcx":"http://standards.iso.org/iso/19115/-3/gcx/1.0",
            "gex":"http://standards.iso.org/iso/19115/-3/gex/1.0",
            "lan":"http://standards.iso.org/iso/19115/-3/lan/1.0",
            "srv":"http://standards.iso.org/iso/19115/-3/srv/2.0",
            "mas":"http://standards.iso.org/iso/19115/-3/mas/1.0",
            "mcc":"http://standards.iso.org/iso/19115/-3/mcc/1.0",
            "mco":"http://standards.iso.org/iso/19115/-3/mco/1.0",
            "mda":"http://standards.iso.org/iso/19115/-3/mda/1.0",
            "mds":"http://standards.iso.org/iso/19115/-3/mds/1.0",
            "mdt":"http://standards.iso.org/iso/19115/-3/mdt/1.0",
            "mex":"http://standards.iso.org/iso/19115/-3/mex/1.0",
            "mmi":"http://standards.iso.org/iso/19115/-3/mmi/1.0",
            "mpc":"http://standards.iso.org/iso/19115/-3/mpc/1.0",
            "mrc":"http://standards.iso.org/iso/19115/-3/mrc/1.0",
            "mrd":"http://standards.iso.org/iso/19115/-3/mrd/1.0",
            "mri":"http://standards.iso.org/iso/19115/-3/mri/1.0",
            "mrl":"http://standards.iso.org/iso/19115/-3/mrl/1.0",
            "mrs":"http://standards.iso.org/iso/19115/-3/mrs/1.0",
            "msr":"http://standards.iso.org/iso/19115/-3/msr/1.0",
            "mdq":"http://standards.iso.org/iso/19157/-2/mdq/1.0",
            "mac":"http://standards.iso.org/iso/19115/-3/mac/1.0",
            "gco":"http://standards.iso.org/iso/19115/-3/gco/1.0",
            "gml":"http://www.opengis.net/gml",
            "xlink":"http://www.w3.org/1999/xlink",
            "xsi":"http://www.w3.org/2001/XMLSchema-instance"
        }

        self.inspire_namespaces = {
        }

        self.repository = {
            'mdb:MD_Metadata': {
                'outputschema': 'http://standards.iso.org/iso/19115/-3/mdb/2.0',
                'queryables': {
                    'SupportedISOQueryables': {
                        'mdb:Subject': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:topicCategory/mri:MD_TopicCategoryCode',
                                        'dbcol': self.context.md_core_model['mappings']['pycsw:Keywords']},
                        'mdb:Title': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:citation/cit:CI_Citation/cit:title/gco:CharacterString',
                                      'dbcol': self.context.md_core_model['mappings']['pycsw:Title']},
                        'mdb:Abstract': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:abstract/gco:CharacterString',
                                         'dbcol': self.context.md_core_model['mappings']['pycsw:Abstract']},
                        'mdb:Edition': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:citation/cit:CI_Citation/cit:edition/gco:CharacterString',
                                        'dbcol': self.context.md_core_model['mappings']['pycsw:Edition']},
                        'mdb:Format': {'xpath': 'mdb:distributionInfo/mrd:MD_Distribution/mrd:distributionFormat/mrd:MD_Format/mrd:formatSpecificationCitation/cit:CI_Citation/cit:title/gcx:Anchor',
                                       'dbcol': self.context.md_core_model['mappings']['pycsw:Format']},
                        'mdb:Identifier': {'xpath': 'mdb:metadataIdentifier/mcc:MD_Identifier/mcc:code/gco:CharacterString',
                                           'dbcol': self.context.md_core_model['mappings']['pycsw:Identifier']},
                        'mdb:Modified': {'xpath': 'mdb:MD_Metadata/mdb:dateInfo/cit:CI_Date[cit:dateType/cit:CI_DateTypeCode="lastUpdate"]/cit:date/gco:DateTime',
                                         'dbcol': self.context.md_core_model['mappings']['pycsw:Modified']},
                        'mdb:Type': {'xpath': 'mdb:metadataScope/mdb:MD_MetadataScope/mdb:resourceScope/mcc:MD_ScopeCode/@codeListValue',
                                     'dbcol': self.context.md_core_model['mappings']['pycsw:Type']},
                        # NB: Placeholder only
                        'mdb:BoundingBox': {'xpath': 'mdb:BoundingBox', 'dbcol': self.context.md_core_model['mappings']['pycsw:BoundingBox']},
                        # TODO: find out why this data is missing
                        'mdb:VertExtentMin': {'xpath': 'gex:EX_VerticalExtent/gex:minimumValue/gco:Real', 'dbcol': self.context.md_core_model['mappings']['pycsw:VertExtentMin']},
                        'mdb:VertExtentMax': {'xpath': 'gex:EX_VerticalExtent/gex:maximumValue/gco:Real', 'dbcol': self.context.md_core_model['mappings']['pycsw:VertExtentMax']},
                        'mdb:CRS': {'xpath': '''concat("urn:ogc:def:crs:",
                                                       "mdb:referenceSystemInfo/mrs:MD_ReferenceSystem/mrs:referenceSystemIdentifier/mcc:MD_Identifier/mcc:codeSpace/gco:CharacterString",
                                                       ":",
                                                       "mdb:referenceSystemInfo/mrs:MD_ReferenceSystem/mrs:referenceSystemIdentifier/mcc:MD_Identifier/mcc:version/gco:CharacterString",
                                                       ":",
                                                       "mdb:referenceSystemInfo/mrs:MD_ReferenceSystem/mrs:referenceSystemIdentifier/mcc:MD_Identifier/mcc:code/gco:CharacterString")''',
                                    'dbcol': self.context.md_core_model['mappings']['pycsw:CRS']},
                        'mdb:AlternateTitle': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:citation/cit:CI_Citation/cit:title/gco:CharacterString',
                                               'dbcol': self.context.md_core_model['mappings']['pycsw:AlternateTitle']},
                        'mdb:RevisionDate': {'xpath': 'mdb:dateInfo/cit:CI_Date[cit:dateType/cit:CI_DateTypeCode/@codeListValue="revision"]/cit:date/gco:DateTime',
                                             'dbcol': self.context.md_core_model['mappings']['pycsw:RevisionDate']},
                        'mdb:CreationDate': {'xpath': 'mdb:dateInfo/cit:CI_Date[cit:dateType/cit:CI_DateTypeCode/@codeListValue="creation"]/cit:date/gco:DateTime',
                                             'dbcol': self.context.md_core_model['mappings']['pycsw:CreationDate']},
                        'mdb:PublicationDate': {'xpath': 'mdb:dateInfo/cit:CI_Date[cit:dateType/cit:CI_DateTypeCode/@codeListValue="publication"]/cit:date/gco:DateTime',
                                                'dbcol': self.context.md_core_model['mappings']['pycsw:PublicationDate']},
                        'mdb:OrganisationName': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:pointOfContact/cit:CI_Responsibility/cit:party/cit:CI_Organisation/cit:name/gco:CharacterString',
                                                 'dbcol': self.context.md_core_model['mappings']['pycsw:OrganizationName']},
                        'mdb:HasSecurityConstraints': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:resourceConstraints/mco:MD_SecurityConstraints',
                                                       'dbcol': self.context.md_core_model['mappings']['pycsw:SecurityConstraints']},
                        'mdb:Language': {'xpath': 'mdb:defaultLocale/lan:PT_Locale/lan:language/lan:LanguageCode|mdb:defaultLocale/lan:PT_Locale/lan:language/gco:CharacterString',
                                         'dbcol': self.context.md_core_model['mappings']['pycsw:Language']},
                        'mdb:ParentIdentifier': {'xpath': 'mdb:parentMetadata/cit:CI_Citation/cit:identifier/mcc:MD_Identifier/mcc:code/gco:CharacterString',
                                                 'dbcol': self.context.md_core_model['mappings']['pycsw:ParentIdentifier']},
                        'mdb:KeywordType': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:descriptiveKeywords/mri:MD_Keywords/mri:type/mri:MD_KeywordTypeCode',
                                            'dbcol': self.context.md_core_model['mappings']['pycsw:KeywordType']},
                        'mdb:TopicCategory': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:topicCategory/mri:MD_TopicCategoryCode',
                                              'dbcol': self.context.md_core_model['mappings']['pycsw:TopicCategory']},
                        'mdb:ResourceLanguage': {'xpath': 'mdb:defaultLocale/lan:PT_Locale/lan:language/lan:LanguageCode/@codeListValue',
                                                 'dbcol': self.context.md_core_model['mappings']['pycsw:ResourceLanguage']},
                        'mdb:GeographicDescriptionCode': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:extent/gex:EX_Extent/gex:geographicElement/gex:EX_GeographicDescription/gex:geographicIdentifier/mcc:MD_Identifier/mcc:code/gco:CharacterString',
                                                          'dbcol': self.context.md_core_model['mappings']['pycsw:GeographicDescriptionCode']},
                        'mdb:Denominator': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:spatialResolution/mri:MD_Resolution/mri:equivalentScale/mri:MD_RepresentativeFraction/mri:denominator/gco:Integer',
                                            'dbcol': self.context.md_core_model['mappings']['pycsw:Denominator']},
                        'mdb:DistanceValue': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:spatialResolution/mri:MD_Resolution/mri:distance/gco:Distance',
                                              'dbcol': self.context.md_core_model['mappings']['pycsw:DistanceValue']},
                        'mdb:DistanceUOM': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:spatialResolution/mri:MD_Resolution/mri:distance/gco:Distance/@uom',
                                            'dbcol': self.context.md_core_model['mappings']['pycsw:DistanceUOM']},
                        'mdb:TempExtent_begin': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:extent/gex:EX_Extent/gex:temporalElement/gex:EX_TemporalExtent/mri:extent/gml:TimePeriod/gml:beginPosition',
                                                 'dbcol': self.context.md_core_model['mappings']['pycsw:TempExtent_begin']},
                        'mdb:TempExtent_end': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:extent/gex:EX_Extent/gex:temporalElement/gex:EX_TemporalExtent/mri:extent/gml:TimePeriod/gml:endPosition',
                                               'dbcol': self.context.md_core_model['mappings']['pycsw:TempExtent_end']},
                        'mdb:AnyText': {'xpath': '//',
                                        'dbcol': self.context.md_core_model['mappings']['pycsw:AnyText']},
                        'mdb:ServiceType': {'xpath': 'mdb:identificationInfo/srv:SV_ServiceIdentification/srv:serviceType/gco:LocalName',
                                            'dbcol': self.context.md_core_model['mappings']['pycsw:ServiceType']},
                        'mdb:ServiceTypeVersion': {'xpath': 'mdb:identificationInfo/srv:SV_ServiceIdentification/srv:serviceTypeVersion/gco:CharacterString',
                                                   'dbcol': self.context.md_core_model['mappings']['pycsw:ServiceTypeVersion']},
                        'mdb:Operation': {'xpath': 'mdb:identificationInfo/srv:SV_ServiceIdentification/srv:containsOperations/srv:SV_OperationMetadata/srv:operationName/gco:CharacterString',
                                          'dbcol': self.context.md_core_model['mappings']['pycsw:Operation']},
                        'mdb:CouplingType': {'xpath': 'mdb:identificationInfo/srv:SV_ServiceIdentification/srv:couplingType/srv:SV_CouplingType',
                                             'dbcol': self.context.md_core_model['mappings']['pycsw:CouplingType']},
                        'mdb:OperatesOn': {'xpath': 'mdb:identificationInfo/srv:SV_ServiceIdentification/srv:operatesOn/mri:MD_DataIdentification/mri:citation/cit:CI_Citation/cit:identifier/mcc:MD_Identifier/mcc:code/gco:CharacterString',
                                           'dbcol': self.context.md_core_model['mappings']['pycsw:OperatesOn']},
                        'mdb:OperatesOnIdentifier': {'xpath': 'mdb:identificationInfo/srv:SV_ServiceIdentification/srv:coupledResource/srv:SV_CoupledResource/srv:identifier/gco:CharacterString',
                                                     'dbcol': self.context.md_core_model['mappings']['pycsw:OperatesOnIdentifier']},
                        'mdb:OperatesOnName': {'xpath': 'mdb:identificationInfo/srv:SV_ServiceIdentification/srv:coupledResource/srv:SV_CoupledResource/srv:operationName/gco:CharacterString',
                                               'dbcol': self.context.md_core_model['mappings']['pycsw:OperatesOnName']},
                    },
                    'AdditionalQueryables': {
                        'mdb:Degree': {'xpath': 'mdb:dataQualityInfo/mdq:DQ_DataQuality/mdq:report/mdq:DQ_DomainConsistency/mdq:result/mdq:DQ_ConformanceResult/mdq:pass/gco:Boolean',
                                       'dbcol': self.context.md_core_model['mappings']['pycsw:Degree']},
                        'mdb:AccessConstraints': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:resourceConstraints/mco:MD_LegalConstraints/mco:accessConstraints/mco:MD_RestrictionCode',
                                                  'dbcol': self.context.md_core_model['mappings']['pycsw:AccessConstraints']},
                        'mdb:OtherConstraints': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:resourceConstraints/mco:MD_LegalConstraints/mco:otherConstraints/gco:CharacterString',
                                                 'dbcol': self.context.md_core_model['mappings']['pycsw:OtherConstraints']},
                        'mdb:Classification': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:resourceConstraints/mco:MD_LegalConstraints/mco:accessConstraints/mco:MD_ClassificationCode/@codeListValue',
                                               'dbcol': self.context.md_core_model['mappings']['pycsw:Classification']},
                        'mdb:ConditionApplyingToAccessAndUse': {'xpath': 'mdb:metadataConstraints/mco:MD_LegalConstraints/mco:useLimitation/gco:CharacterString|mdb:identificationInfo/mri:MD_DataIdentification/mri:resourceConstraints/mco:MD_LegalConstraints/mco:useLimitation/gco:CharacterString',
                                                                'dbcol': self.context.md_core_model['mappings']['pycsw:ConditionApplyingToAccessAndUse']},
                        'mdb:Lineage': {'xpath': 'mdb:dataQualityInfo/mdq:DQ_DataQuality/mrl:lineage/mrl:LI_Lineage/mrl:statement/gco:CharacterString',
                                        'dbcol': self.context.md_core_model['mappings']['pycsw:Lineage']},
                        'mdb:ResponsiblePartyRole': {'xpath': 'mdb:contact/cit:CI_Responsiblility/cit:role/cit:CI_RoleCode',
                                                     'dbcol': self.context.md_core_model['mappings']['pycsw:ResponsiblePartyRole']},
                        'mdb:SpecificationTitle': {'xpath': 'mdb:dataQualityInfo/mdq:DQ_DataQuality/mdq:report/mdq:DQ_DomainConsistency/mdq:result/mdq:DQ_ConformanceResult/mdq:specification/cit:CI_Citation/cit:title/gco:CharacterString',
                                                   'dbcol': self.context.md_core_model['mappings']['pycsw:SpecificationTitle']},
                        'mdb:SpecificationDate': {'xpath': 'mdb:dataQualityInfo/mdq:DQ_DataQuality/mdq:report/mdq:DQ_DomainConsistency/mdq:result/mdq:DQ_ConformanceResult/mdq:secification/cit:CI_Citation/cit:date/cit:CI_Date/cit:date/gco:Date',
                                                  'dbcol': self.context.md_core_model['mappings']['pycsw:SpecificationDate']},
                        'mdb:SpecificationDateType': {'xpath': 'mdb:dataQualityInfo/mdq:DQ_DataQuality/mdq:report/mdq:DQ_DomainConsistency/mdq:result/mdq:DQ_ConformanceResult/mdq:specification/cit:CI_Citation/cit:date/cit:CI_Date/cit:dateType/cit:CI_DateTypeCode/@codeListValue',
                                                      'dbcol': self.context.md_core_model['mappings']['pycsw:SpecificationDateType']},
        
                        'mdb:Creator': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:citation/cit:CI_Citation/cit:citedResponsibleParty/cit:CI_Responsibility/cit:role/cit:CI_RoleCode[text()="creator"]',
                                        'dbcol': self.context.md_core_model['mappings']['pycsw:Creator']},
                        'mdb:Publisher': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:citation/cit:CI_Citation/cit:citedResponsibleParty/cit:CI_Responsibility/cit:role/cit:CI_RoleCode[text()="publisher"]',
                                          'dbcol': self.context.md_core_model['mappings']['pycsw:Publisher']},
                        'mdb:Contributor': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:citation/cit:CI_Citation/cit:citedResponsibleParty/cit:CI_Responsibility/cit:role/cit:CI_RoleCode[text()="contributor"]',
                                            'dbcol': self.context.md_core_model['mappings']['pycsw:Contributor']},
                        'mdb:Relation': {'xpath': 'mdb:identificationInfo/mri:MD_DataIdentification/mri:aggregationInfo',
                                         'dbcol': self.context.md_core_model['mappings']['pycsw:Relation']},
                        # 19115-2
                        'mdb:Platform': {'xpath': 'mdb:acquisitionInfo/mac:MI_AcquisitionInformation/mac:platform/mac:MI_Platform/mac:identifier',
                                         'dbcol': self.context.md_core_model['mappings']['pycsw:Platform']},
                        'mdb:Instrument': {'xpath': 'mdb:acquisitionInfo/mac:MI_AcquisitionInformation/mac:platform/mac:MI_Platform/mac:instrument/mac:MI_Instrument/mac:identifier',
                                           'dbcol': self.context.md_core_model['mappings']['pycsw:Instrument']},
                        'mdb:SensorType': {'xpath': 'mdb:acquisitionInfo/mac:MI_AcquisitionInformation/mac:platform/mac:MI_Platform/mac:instrument/mac:MI_Instrument/mac:type',
                                           'dbcol': self.context.md_core_model['mappings']['pycsw:SensorType']}, 
                        'mdb:CloudCover': {'xpath': 'mdb:contentInfo/mrc:MD_ImageDescription/mrc:cloudCoverPercentage',
                                           'dbcol': self.context.md_core_model['mappings']['pycsw:CloudCover']},
                        'mdb:Bands': {'xpath': 'mdb:contentInfo/mrc:MD_ImageDescription/mrc:attributeGroup/mrc:MD_AttributeGroup/mrc:attribute/mrc:MD_Band/mrc:sequenceIdentifier/gco:MemberName/gco:aName/gco:CharacterString',
                                      'dbcol': self.context.md_core_model['mappings']['pycsw:Bands']},
                    }
                },
                'mappings': {
                    'csw:Record': {
                        # map MDB queryables to DC queryables
                        'mdb:Title': 'dc:title',
                        'mdb:Creator': 'dc:creator',
                        'mdb:Subject': 'dc:subject',
                        'mdb:Abstract': 'dct:abstract',
                        'mdb:Publisher': 'dc:publisher',
                        'mdb:Contributor': 'dc:contributor',
                        'mdb:Modified': 'dct:modified',
                        'mdb:PublicationDate': 'dc:date',
                        'mdb:Type': 'dc:type',
                        'mdb:Format': 'dc:format',
                        'mdb:Language': 'dc:language',
                        'mdb:Relation': 'dc:relation',
                        'mdb:AccessConstraints': 'dc:rights',
                    }
                }
            }
        }

        profile.Profile.__init__(self,
            name='ga',
            version='1.0.0',
            title='GA Profile of ISO 19115-3 XML Metadata',
            url='http://ga.gov.au',
            namespace=self.namespaces['mdb'],
            typename='mdb:MD_Metadata',
            outputschema='http://standards.iso.org/iso/19115/-3/mdb/2.0',
            prefixes=['mdb'],
            model=model,
            core_namespaces=namespaces,
            added_namespaces=self.namespaces,
            repository=self.repository['mdb:MD_Metadata'])

    def extend_core(self, model, namespaces, config):
        """ Extend core configuration

        :param model:
        """

        # update harvest resource types with WMS, since WMS is not a typename,
        if 'Harvest' in model['operations']:
            model['operations']['Harvest']['parameters']['ResourceType']['values'].append('https://schemas.isotc211.org/19115/-3/mdb/1.0/')

        self.inspire_config = None

        server_cfg = config["server"]
        self.ogc_schemas_base = server_cfg.get('ogc_schemas_base', 'http://schemas.opengis.net')
        self.url = server_cfg.get('url', 'http://localhost/pycsw/csw.py')

    def check_parameters(self, kvp):
        """ Check for Language parameter in GetCapabilities request
            Kept for backwards compatibility
        """
        return None

    def get_extendedcapabilities(self):
        """ Get extended capabilities
            Kept for backwards compatibility
        """
        return None

    def get_schemacomponents(self):
        """ Return schema components as lxml.etree.Element list
        """

        node1 = etree.Element(
        util.nspath_eval('csw:SchemaComponent', self.context.namespaces),
        schemaLanguage='XMLSCHEMA', targetNamespace=self.namespace,
        parentSchema='mdb.xsd')

        # Copied from: https://github.com/geonetwork/core-geonetwork/tree/main/schemas/iso19115-3.2018/src/main/plugin/iso19115-3.2018/schema/standards.iso.org/19115/-3/mdb/1.0
        schema_file = os.path.join(self.context.pycsw_home, 'plugins',
                                   'profiles', 'iso19115p3', 'schemas', 'ogc',
                                   'iso', 'iso19115-3', 'mdb', '1.0', 'mdb.xsd')

        schema = etree.parse(schema_file, self.context.parser).getroot()

        node1.append(schema)

        node2 = etree.Element(
        util.nspath_eval('csw:SchemaComponent', self.context.namespaces),
        schemaLanguage='XMLSCHEMA', targetNamespace=self.namespace,
        parentSchema='mdb.xsd')

        schema_file = os.path.join(self.context.pycsw_home, 'plugins',
                                   'profiles', 'iso19115p3', 'schemas', 'ogc',
                                   'iso', 'iso19115-3', 'srv', '2.0',
                                   'serviceInformation.xsd')

        schema = etree.parse(schema_file, self.context.parser).getroot()

        node2.append(schema)

        return [node1, node2]

    def check_getdomain(self, kvp):
        """ Perform extra profile specific checks in the GetDomain request
            Kept for backwards compatibility
        """
        return None

    def write_record(self, result, esn, outputschema, queryables, caps=None):
        """ Return csw:SearchResults child as etree.Element

        :param result: results from repository query (to be written out)
        :param esn: CSW element set name parameter
        :param outputschema: CSW outputschema
        :param queryables: database column mapping for our 'mdb:XXXX'
        :param caps: optional information object gathered from GetCapabilities response
        """
        typename = util.getqattr(result, self.context.md_core_model['mappings']['pycsw:Typename'])
        is_mdb_anyway = False

        xml_blob = util.getqattr(result, self.context.md_core_model['mappings']['pycsw:XML'])

        #xml_blob_decoded = bytes.fromhex(xml_blob[2:]).decode('utf-8')

        if isinstance(xml_blob, bytes):
            iso_string = b'<mdb:MD_Metadata>'
        else:
            iso_string = '<mdb:MD_Metadata>'

        if caps is None and xml_blob is not None and xml_blob.startswith(iso_string):
            is_mdb_anyway = True

        if (esn == 'full' and (typename == 'mdb:MD_Metadata' or is_mdb_anyway)):
            # dump record as is and exit
            return etree.fromstring(xml_blob, self.context.parser)

        node = etree.Element(util.nspath_eval('mdb:MD_Metadata', self.namespaces), nsmap=self.namespaces)
        node.attrib[util.nspath_eval('xsi:schemaLocation', self.context.namespaces)] = \
                                           f"{self.namespace} {self.ogc_schemas_base}/csw/2.0.2/csw.xsd"

        # metadataIdentifier
        record_id = util.getqattr(result, self.context.md_core_model['mappings']['pycsw:Identifier']).strip()
        self._write_string(node, ['mdb:metadataIdentifier', 'mcc:MD_Identifier', 'mcc:code'], record_id)

        if esn in ['summary', 'full']:
            # defaultLocale
            # Language must use a code, so preferentially prefer to use 'mdb:ResourceLanguage' which maps to 'gmd:MD_LanguageTypeCode' in older ISO XML standard
            try:
                val = util.getqattr(result, queryables['mdb:ResourceLanguage']['dbcol'])
            except Exception as e:
                print(f"{queryables=}")
                print("exc=", e)
            if val is None:
                val = util.getqattr(result, queryables['mdb:Language']['dbcol'])

            pt_locale = build_path(node,['mdb:defaultLocale', 'lan:PT_Locale'], self.namespaces)
            lang_code = build_path(pt_locale,['lan:language', 'lan:LanguageCode'], self.namespaces)
            lang_code.set('codeList', 'http://www.loc.gov/standards/iso639-2/')
            lang_code.set('codeListValue', val)
            self._write_code(pt_locale, ['lan:characterEncoding'], 'lan:MD_CharacterSetCode', 'utf8')

        # metadataScope
        mtype = util.getqattr(result, queryables['mdb:Type']['dbcol']) or None
        if mtype is not None:
            if mtype == 'http://purl.org/dc/dcmitype/Dataset':
                mtype = 'dataset'
            self._write_code(node, ['mdb:metadataScope', 'mdb:MD_MetadataScope', 'mdb:resourceScope'], 'mcc:MD_ScopeCode', mtype)

        if esn in ['summary', 'full']:
            # ontact
            ci_resp = build_path(node, ['mdb:contact', 'cit:CI_Responsibility'], self.namespaces)
            self._write_code(ci_resp, ['cit:role'], 'cit:CI_RoleCode', 'pointOfContact')
            self._write_party_org_gssa(ci_resp)
            self._write_party_point_of_contact(ci_resp)

            # dateInfo - Creation date
            val = util.getqattr(result, queryables['mdb:CreationDate']['dbcol'])
            if val is not None:
                self._write_date(node, 'mdb:dateInfo', 'creation', val)

            # dateInfo - Publication date
            val = util.getqattr(result, queryables['mdb:Modified']['dbcol'])
            if val is not None:
                self._write_date(node, 'mdb:dateInfo', 'revision', val)

            # dateInfo - Revision date
            val = util.getqattr(result, queryables['mdb:PublicationDate']['dbcol'])
            if val is not None:
                self._write_date(node, 'mdb:dateInfo', 'publication', val)
            
            # metadataStandard
            self._write_string(node, ['mdb:metadataStandard', 'cit:CI_Citation', 'cit:title'], 'ISO19119:2016' if mtype == 'service' else 'GA Profile of ISO 19115-1:2014')

        # identificationInfo
        data_service_identification = build_path(node, ['mdb:identificationInfo', 'srv:SV_ServiceIdentification' if mtype == 'service' else 'mri:MD_DataIdentification'], self.namespaces)
        identification_citation = build_path(data_service_identification, ['mri:citation', 'cit:CI_Citation'], self.namespaces)
        self._write_string(identification_citation, ['cit:title'], util.getqattr(result, queryables['mdb:Title']['dbcol']).strip() or '')

        identification_citation_identifier = build_path(identification_citation, ['cit:identifier', 'mcc:MD_Identifier'], self.namespaces)
        self._write_string(identification_citation_identifier, ['mcc:code'], 'https://pid.uat.sarig.sa.gov.au/dataset/' + record_id)
        self._write_string(identification_citation_identifier, ['mcc:codeSpace'], 'GSSA Persistent Identifier')

        if esn in ['summary', 'full']:
            # Abstract
            val = util.getqattr(result, queryables['mdb:Abstract']['dbcol']) or ''
            build_path(data_service_identification, ['mri:abstract', 'gco:CharacterString'], self.namespaces).text = val

            # Point of Contact
            identification_poc_resp = build_path(data_service_identification, ['mri:pointOfContact', 'cit:CI_Responsibility'], self.namespaces)
            self._write_code(identification_poc_resp, ['cit:role'], 'cit:CI_RoleCode', 'pointOfContact')
            self._write_party_point_of_contact(identification_poc_resp)

            # Topic category
            val = util.getqattr(result, queryables['mdb:TopicCategory']['dbcol'])
            if val is None:
                val = "geoscientificInformation"
            build_path(data_service_identification, ['mri:topicCategory', 'mri:MD_TopicCategoryCode'], self.namespaces).text = 'geoscientificInformation'  # TODO: update to lookup value

            # Spatial resolution
            val = util.getqattr(result, queryables['mdb:Denominator']['dbcol'])
            if val:
                path = ['mri:spatialResolution', 'mri:MD_Resolution', 'mri:equivalentScale',
                        'mri:MD_RepresentativeFraction', 'mri:denominator', 'gco:Integer']
                int_elem = build_path(data_service_identification, path, self.namespaces)
                int_elem.text = str(val)

        # Bbox and vertical extent
        bbox = util.getqattr(result, queryables['mdb:BoundingBox']['dbcol'])
        vert_ext_min = util.getqattr(result, queryables['mdb:VertExtentMin']['dbcol'])
        vert_ext_max = util.getqattr(result, queryables['mdb:VertExtentMax']['dbcol'])
        # Convert float to string
        if vert_ext_min is not None:
            vert_ext_min = f"{vert_ext_min}"
        if vert_ext_max is not None:
            vert_ext_max = f"{vert_ext_max}"
        bboxel = self._write_extent(bbox, vert_ext_min, vert_ext_max)
        if bboxel is not None and mtype != 'service':
            # Add <mri:extent> element etc.
            data_service_identification.append(bboxel)

        if esn in ['summary', 'full']:
            # resourceMaintenance
            self._write_code(
                data_service_identification,
                ['mri:resourceMaintenance', 'mmi:MD_MaintenanceInformation', 'mmi:maintenanceAndUpdateFrequency'],
                'mmi:MD_MaintenanceFrequencyCode', 'asNeeded'  # TODO: read real value
            )

            # resourceFormat
            identification_resource_format = build_path(
                data_service_identification,
                ['mri:resourceFormat', 'mrd:MD_Format', 'mrd:formatSpecificationCitation', 'cit:CI_Citation'],
                self.namespaces
            )
            self._write_string(identification_resource_format, ['cit:title'], 'Product data repository: Various Formats')  # TODO: read real value
            online_resource = build_path(
                identification_resource_format,
                ['cit:onlineResource', 'cit:CI_OnlineResource'],
                self.namespaces
            )
            self._write_string(online_resource, ['cit:linkage'], 'file://prod.lan/active/ops/cds/records/Rec2018_026')  # TODO: read real value
            protocol = build_path(online_resource, ['cit:protocol', 'gco:CharacterString'], self.namespaces)
            protocol.text = 'WWW:LINK-1.0-http--link'
            protocol.attrib[util.nspath_eval('xsi:type', self.context.namespaces)] = 'gco:CodeType'
            protocol.attrib['codeSpace'] = 'http://pid.geoscience.gov.au/def/schema/ga/ISO19115-3-2016/codelist/ga_profile_codelists.xml#gapCI_ProtocolTypeCode'
            # self._add_string_value(online_resource, ['cit:name'], 'WWW:LINK')  # TODO: read real value
            # self._add_string_value(online_resource, ['cit:description'], 'WWW:LINK')  # TODO: read real value

        # Keywords
        kw = util.getqattr(result, queryables['mdb:Subject']['dbcol'])
        if kw is not None:
            md_keywords = build_path(data_service_identification, ['mri:descriptiveKeywords'], self.namespaces)
            md_keywords.append(self._write_keywords(kw))

        # resourceConstraints - Legal
        resource_constraints_xml = """
        <mri:resourceConstraints
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:cit="http://standards.iso.org/iso/19115/-3/cit/1.0"
            xmlns:gex="http://standards.iso.org/iso/19115/-3/gex/1.0"
            xmlns:lan="http://standards.iso.org/iso/19115/-3/lan/1.0"
            xmlns:mcc="http://standards.iso.org/iso/19115/-3/mcc/1.0"
            xmlns:mco="http://standards.iso.org/iso/19115/-3/mco/1.0"
            xmlns:mdb="http://standards.iso.org/iso/19115/-3/mdb/1.0"
            xmlns:mmi="http://standards.iso.org/iso/19115/-3/mmi/1.0"
            xmlns:mrd="http://standards.iso.org/iso/19115/-3/mrd/1.0"
            xmlns:mri="http://standards.iso.org/iso/19115/-3/mri/1.0"
            xmlns:mrl="http://standards.iso.org/iso/19115/-3/mrl/1.0"
            xmlns:gco="http://standards.iso.org/iso/19115/-3/gco/1.0"        
        >
            <mco:MD_LegalConstraints uuid="urn:ga-licences:232">
                <mco:reference>
                    <cit:CI_Citation>
                        <cit:title>
                            <gco:CharacterString>Creative Commons Attribution 4.0 International Licence</gco:CharacterString>
                        </cit:title>
                        <cit:alternateTitle>
                            <gco:CharacterString>CC-BY</gco:CharacterString>
                        </cit:alternateTitle>
                        <cit:edition>
                            <gco:CharacterString>4.0</gco:CharacterString>
                        </cit:edition>
                        <cit:onlineResource>
                            <cit:CI_OnlineResource>
                                <cit:linkage>
                                    <gco:CharacterString>http://creativecommons.org/licenses/</gco:CharacterString>
                                </cit:linkage>
                                <cit:protocol>
                                    <gco:CharacterString xsi:type="gco:CodeType"
                                                         codeSpace="http://pid.geoscience.gov.au/def/schema/ga/ISO19115-3-2016/codelist/ga_profile_codelists.xml#gapCI_ProtocolTypeCode">
                                        WWW:LINK-1.0-http--link
                                    </gco:CharacterString>
                                </cit:protocol>
                            </cit:CI_OnlineResource>
                        </cit:onlineResource>
                    </cit:CI_Citation>
                </mco:reference>
                <mco:accessConstraints>
                    <mco:MD_RestrictionCode codeList="codeListLocation#MD_RestrictionCode" codeListValue="license"/>
                </mco:accessConstraints>
                <mco:useConstraints>
                    <mco:MD_RestrictionCode codeList="codeListLocation#MD_RestrictionCode" codeListValue="license"/>
                </mco:useConstraints>
            </mco:MD_LegalConstraints>
        </mri:resourceConstraints>
        """
        data_service_identification.append(etree.fromstring(resource_constraints_xml))

        # resourceConstraints - Security
        md_security_constraints = """
        <mco:MD_SecurityConstraints>
            <mco:reference>
                <cit:CI_Citation>
                    <cit:title>
                        <gco:CharacterString>Australian Government Security Classification System</gco:CharacterString>
                    </cit:title>
                    <cit:editionDate>
                        <gco:DateTime>2018-11-01T00:00:00</gco:DateTime>
                    </cit:editionDate>
                    <cit:onlineResource>
                        <cit:CI_OnlineResource>
                            <cit:linkage>
                                <gco:CharacterString>https://www.protectivesecurity.gov.au/Pages/default.aspx</gco:CharacterString>
                            </cit:linkage>
                            <cit:protocol>
                                <gco:CharacterString xsi:type="gco:CodeType" codeSpace="http://pid.geoscience.gov.au/def/schema/ga/ISO19115-3-2016/codelist/ga_profile_codelists.xml#gapCI_ProtocolTypeCode">WWW:LINK-1.0-http--link</gco:CharacterString>
                            </cit:protocol>
                        </cit:CI_OnlineResource>
                    </cit:onlineResource>
                </cit:CI_Citation>
            </mco:reference>
            <mco:classification>
                <mco:MD_ClassificationCode codeList="codeListLocation#MD_ClassificationCode" codeListValue="unclassified"/>
            </mco:classification>  
        </mco:MD_SecurityConstraints>      
        """
        resource_constraints_xml2 = f"""
        <mri:resourceConstraints
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:cit="http://standards.iso.org/iso/19115/-3/cit/1.0"
            xmlns:gex="http://standards.iso.org/iso/19115/-3/gex/1.0"
            xmlns:lan="http://standards.iso.org/iso/19115/-3/lan/1.0"
            xmlns:mcc="http://standards.iso.org/iso/19115/-3/mcc/1.0"
            xmlns:mco="http://standards.iso.org/iso/19115/-3/mco/1.0"
            xmlns:mdb="http://standards.iso.org/iso/19115/-3/mdb/1.0"
            xmlns:mmi="http://standards.iso.org/iso/19115/-3/mmi/1.0"
            xmlns:mrd="http://standards.iso.org/iso/19115/-3/mrd/1.0"
            xmlns:mri="http://standards.iso.org/iso/19115/-3/mri/1.0"
            xmlns:mrl="http://standards.iso.org/iso/19115/-3/mrl/1.0"
            xmlns:gco="http://standards.iso.org/iso/19115/-3/gco/1.0"        
        >
            {md_security_constraints}
        </mri:resourceConstraints>
        """
        data_service_identification.append(etree.fromstring(resource_constraints_xml2))

        # Service identification
        if mtype == 'service':
            # Service type & service type version
            val = util.getqattr(result, queryables['mdb:ServiceType']['dbcol'])
            val2 = util.getqattr(result, queryables['mdb:ServiceTypeVersion']['dbcol'])
            if val is not None:
                tmp = etree.SubElement(identification_citation, util.nspath_eval('srv:serviceType', self.namespaces))
                etree.SubElement(tmp, util.nspath_eval('gco:LocalName', self.namespaces)).text = val
                tmp = etree.SubElement(identification_citation, util.nspath_eval('srv:serviceTypeVersion', self.namespaces))
                etree.SubElement(tmp, util.nspath_eval('gco:CharacterString', self.namespaces)).text = val2

            # Keywords
            kw = util.getqattr(result, queryables['mdb:Subject']['dbcol'])
            if kw is not None:
                srv_keywords = etree.SubElement(identification_citation, util.nspath_eval('srv:descriptiveKeywords', self.namespaces))
                srv_keywords.append(self._write_keywords(kw))

            # Extent and bounding box
            if bboxel is not None:
                # Change <mri:extent> element to <srv:extent> and append
                bboxel.tag = util.nspath_eval('srv:extent', self.namespaces)
                identification_citation.append(bboxel)

            val = util.getqattr(result, queryables['mdb:CouplingType']['dbcol'])
            if val is not None:
                couplingtype = etree.SubElement(identification_citation, util.nspath_eval('srv:couplingType', self.namespaces))
                etree.SubElement(couplingtype, util.nspath_eval('srv:SV_CouplingType', self.namespaces), codeListValue=val, codeList=f'{CODELIST}#SV_CouplingType').text = val

            if esn in ['summary', 'full']:
                # all service resources as coupled resources
                coupledresources = util.getqattr(result, queryables['mdb:OperatesOn']['dbcol'])
                operations = util.getqattr(result, queryables['mdb:Operation']['dbcol'])

                if coupledresources:
                    for val2 in coupledresources.split(','):
                        coupledres = etree.SubElement(identification_citation, util.nspath_eval('srv:coupledResource', self.namespaces))
                        svcoupledres = etree.SubElement(coupledres, util.nspath_eval('srv:SV_CoupledResource', self.namespaces))
                        opname = etree.SubElement(svcoupledres, util.nspath_eval('srv:coupledName', self.namespaces))
                        etree.SubElement(opname, util.nspath_eval('gco:ScopedName', self.namespaces)).text = get_resource_opname(operations)
                        sid = etree.SubElement(svcoupledres, util.nspath_eval('srv:resourceReference', self.namespaces))
                        # Unfortunately only have one field to apply 
                        # <srv:resourceReference> has a <cit:CI_Citation>
                        ci_citation = etree.SubElement(sid, util.nspath_eval('cit:CI_Citation', self.namespaces))
                        # <cit:CI_Citation> must have a title, insert reference
                        build_path(ci_citation, ['cit:title', 'gco:CharacterString'],  self.namespaces).text = val2
                        # Insert reference as a identifier code
                        build_path(ci_citation, ['cit:identifer', 'mcc:MD_Identifier', 'mcc:code', 'gco:CharacterString'], self.namespaces).text = val2

                # Service operations
                if operations:
                    for i in operations.split(','):
                        oper = etree.SubElement(identification_citation, util.nspath_eval('srv:containsOperations', self.namespaces))
                        sv_opermetadata = etree.SubElement(oper, util.nspath_eval('srv:SV_OperationMetadata', self.namespaces))

                        oper_name = etree.SubElement(sv_opermetadata, util.nspath_eval('srv:operationName', self.namespaces))
                        etree.SubElement(oper_name, util.nspath_eval('gco:CharacterString', self.namespaces)).text = i
                        
                        dcp = etree.SubElement(sv_opermetadata, util.nspath_eval('srv:distributedComputingPlatform', self.namespaces))
                        dcp_list1 = etree.SubElement(dcp, util.nspath_eval('srv:DCPList', self.namespaces))
                        etree.SubElement(dcp_list1, util.nspath_eval('srv:DCPList', self.namespaces), codeList=f'{CODELIST}#DCPList', codeListValue='HTTPGet').text = 'HTTPGet'

                        dcp_list2 = etree.SubElement(dcp, util.nspath_eval('srv:DCPList', self.namespaces))
                        etree.SubElement(dcp_list2, util.nspath_eval('srv:DCPList', self.namespaces), codeList=f'{CODELIST}#DCPList', codeListValue='HTTPPost').text = 'HTTPPost'

                        connectpoint = etree.SubElement(sv_opermetadata, util.nspath_eval('srv:connectPoint', self.namespaces))
                        onlineres = etree.SubElement(connectpoint, util.nspath_eval('cit:CI_OnlineResource', self.namespaces))
                        linkage = etree.SubElement(onlineres, util.nspath_eval('cit:linkage', self.namespaces))
                        etree.SubElement(linkage, util.nspath_eval('gco:CharacterString', self.namespaces)).text = util.getqattr(result, self.context.md_core_model['mappings']['pycsw:Source'])

                # operates on resource(s)
                if coupledresources:
                    for i in coupledresources.split(','):
                        operates_on = etree.SubElement(identification_citation, util.nspath_eval('srv:operatesOn', self.namespaces))
                        code = build_path(operates_on, ['mri:MD_DataIdentification','mri:citation','cit:CI_Citation','cit:identifier','mcc:MD_Identifier','mcc:code','gcx:Anchor'], self.namespaces)
                        code.text = f"{util.bind_url(self.url)}service=CSW&version=2.0.2&request=GetRecordById&outputschema={self.repository['mdb:MD_Metadata']['outputschema']}&id={record_id}-{i}"

        rlinks = util.getqattr(result, self.context.md_core_model['mappings']['pycsw:Links'])
        if rlinks:
            distinfo = etree.SubElement(node, util.nspath_eval('mdb:distributionInfo', self.namespaces))
            distinfo2 = etree.SubElement(distinfo, util.nspath_eval('mrd:MD_Distribution', self.namespaces))
            transopts = etree.SubElement(distinfo2, util.nspath_eval('mrd:transferOptions', self.namespaces))
            dtransopts = etree.SubElement(transopts, util.nspath_eval('mrd:MD_DigitalTransferOptions', self.namespaces))

            for link in util.jsonify_links(rlinks):
                online = etree.SubElement(dtransopts, util.nspath_eval('mrd:onLine', self.namespaces))
                online2 = etree.SubElement(online, util.nspath_eval('cit:CI_OnlineResource', self.namespaces))

                linkage = etree.SubElement(online2, util.nspath_eval('cit:linkage', self.namespaces))
                etree.SubElement(linkage, util.nspath_eval('gco:CharacterString', self.namespaces)).text = link['url']

                protocol = etree.SubElement(online2, util.nspath_eval('cit:protocol', self.namespaces))
                protocol_char = etree.SubElement(protocol, util.nspath_eval('gco:CharacterString', self.namespaces))
                protocol_char.text = link.get('protocol', 'WWW:LINK-1.0-http--link')
                protocol_char.attrib[util.nspath_eval('xsi:type', self.namespaces)] = "gco:CodeType"
                protocol_char.attrib["codeSpace"] = "http://pid.geoscience.gov.au/def/schema/ga/ISO19115-3-2016/codelist/ga_profile_codelists.xml#gapCI_ProtocolTypeCode"

                name = etree.SubElement(online2, util.nspath_eval('cit:name', self.namespaces))
                etree.SubElement(name, util.nspath_eval('gco:CharacterString', self.namespaces)).text = link.get('name')

                desc = etree.SubElement(online2, util.nspath_eval('cit:description', self.namespaces))
                etree.SubElement(desc, util.nspath_eval('gco:CharacterString', self.namespaces)).text = link.get('description')

        # resourceLineage
        # TODO: replace this placeholder with real lineage
        resource_lineage = """
        <mdb:resourceLineage
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:cit="http://standards.iso.org/iso/19115/-3/cit/1.0"
            xmlns:gex="http://standards.iso.org/iso/19115/-3/gex/1.0"
            xmlns:lan="http://standards.iso.org/iso/19115/-3/lan/1.0"
            xmlns:mcc="http://standards.iso.org/iso/19115/-3/mcc/1.0"
            xmlns:mco="http://standards.iso.org/iso/19115/-3/mco/1.0"
            xmlns:mdb="http://standards.iso.org/iso/19115/-3/mdb/1.0"
            xmlns:mmi="http://standards.iso.org/iso/19115/-3/mmi/1.0"
            xmlns:mrd="http://standards.iso.org/iso/19115/-3/mrd/1.0"
            xmlns:mri="http://standards.iso.org/iso/19115/-3/mri/1.0"
            xmlns:mrl="http://standards.iso.org/iso/19115/-3/mrl/1.0"
            xmlns:gco="http://standards.iso.org/iso/19115/-3/gco/1.0"        
        >
            <mrl:LI_Lineage>
                <mrl:statement>
                    <gco:CharacterString>No lineage is available</gco:CharacterString>
                </mrl:statement>
                <mrl:scope>
                    <mcc:MD_Scope>
                        <mcc:level>
                            <mcc:MD_ScopeCode codeList="codeListLocation#MD_ScopeCode" codeListValue="document"/>
                        </mcc:level>
                    </mcc:MD_Scope>
                </mrl:scope>
            </mrl:LI_Lineage>
        </mdb:resourceLineage>
        """
        node.append(etree.fromstring(resource_lineage))

        # metadataConstraints
        resource_constraints_xml2 = f"""
        <mdb:metadataConstraints
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:cit="http://standards.iso.org/iso/19115/-3/cit/1.0"
            xmlns:gex="http://standards.iso.org/iso/19115/-3/gex/1.0"
            xmlns:lan="http://standards.iso.org/iso/19115/-3/lan/1.0"
            xmlns:mcc="http://standards.iso.org/iso/19115/-3/mcc/1.0"
            xmlns:mco="http://standards.iso.org/iso/19115/-3/mco/1.0"
            xmlns:mdb="http://standards.iso.org/iso/19115/-3/mdb/1.0"
            xmlns:mmi="http://standards.iso.org/iso/19115/-3/mmi/1.0"
            xmlns:mrd="http://standards.iso.org/iso/19115/-3/mrd/1.0"
            xmlns:mri="http://standards.iso.org/iso/19115/-3/mri/1.0"
            xmlns:mrl="http://standards.iso.org/iso/19115/-3/mrl/1.0"
            xmlns:gco="http://standards.iso.org/iso/19115/-3/gco/1.0"        
        >
            {md_security_constraints}
        </mdb:metadataConstraints>
        """
        node.append(etree.fromstring(resource_constraints_xml2))

        return node

    def _write_contact_phone(self, ci_contact, phone_num_str):
        """
        Write out a telephone number of a contact within an organisation

        :param ci_contact: 'cit:CI_Contact' XML etree.Element
        :param phone_num_str: phone number string
        :returns: XML contact phone etree.Element
        """
        phone = build_path(ci_contact, ['cit:phone', 'cit:CI_Telephone'], self.namespaces)
        ph_number = build_path(phone, ['cit:number', 'gco:CharacterString'], self.namespaces)
        ph_number.text = phone_num_str
        ph_type = build_path(phone, ['cit:numberType', 'cit:CI_TelephoneTypeCode'], self.namespaces)
        ph_type.text = "voice"

    def _write_contact_fax(self, ci_contact, fax_num_str):
        """
        Write out a fax number  of a contact within an organisation

        :param ci_contact: 'cit:CI_Contact' XML etree.Element
        :param fax_num_str: fax number string
        :returns: XML contact fax etree.Element
        """
        phone = build_path(ci_contact, ['cit:phone', 'cit:CI_Telephone'], self.namespaces, reuse=False)
        ph_number = build_path(phone, ['cit:number', 'gco:CharacterString'], self.namespaces)
        ph_number.text = fax_num_str
        ph_type = build_path(phone, ['cit:numberType', 'cit:CI_TelephoneTypeCode'], self.namespaces)
        ph_type.text = "facsimile"

    def _write_contact_address(self, ci_resp, ci_contact, **contact):
        """
        Write out an address of a contact within an organisation

        :param ci_resp: 'cit:CI_Responsibility' XML etree.Element
        :param ci_contact: 'cit:CI_Contact' XML etree.Element
        :param contact: dict of contact details, keys are 'address' 'city' 'region' 'postcode' 'country' 'email'
        :returns: XML contact address etree.Element
        """
        ci_address = build_path(ci_contact, ['cit:address', 'cit:CI_Address'], self.namespaces)
        if contact.get('address', None) is not None:
            delivery_point = etree.SubElement(ci_address, util.nspath_eval('cit:deliveryPoint', self.namespaces))
            etree.SubElement(delivery_point, util.nspath_eval('gco:CharacterString', self.namespaces)).text = contact['address']
        if contact.get('city', None) is not None:
            city = etree.SubElement(ci_address, util.nspath_eval('cit:city', self.namespaces))
            etree.SubElement(city, util.nspath_eval('gco:CharacterString', self.namespaces)).text = contact['city']
        if contact.get('region', None) is not None:
            admin_area = etree.SubElement(ci_address, util.nspath_eval('cit:administrativeArea', self.namespaces))
            etree.SubElement(admin_area, util.nspath_eval('gco:CharacterString', self.namespaces)).text = contact['region']
        if contact.get('postcode', None) is not None:
            postal_code = etree.SubElement(ci_address, util.nspath_eval('cit:postalCode', self.namespaces))
            etree.SubElement(postal_code, util.nspath_eval('gco:CharacterString', self.namespaces)).text = contact['postcode']
        if contact.get('country', None)  is not None:
            country = etree.SubElement(ci_address, util.nspath_eval('cit:country', self.namespaces))
            etree.SubElement(country, util.nspath_eval('gco:CharacterString', self.namespaces)).text = contact['country']
        if contact.get('email', None)  is not None:
            email = etree.SubElement(ci_address, util.nspath_eval('cit:electronicMailAddress', self.namespaces))
            etree.SubElement(email, util.nspath_eval('gco:CharacterString', self.namespaces)).text = contact['email']

        # URL of organisation or individual
        if contact.get('url', None) is not None:
            path = ['cit:onlineResource', 'cit:CI_OnlineResource', 'cit:linkage', 'gco:CharacterString']
            url = build_path(ci_contact, path, self.namespaces)
            url.text = contact['url']
        # Role
        role = build_path(ci_resp, ['cit:role', 'cit:CI_RoleCode'], self.namespaces)
        role.set("codeList", f'{CODELIST}#CI_RoleCode')
        role_str = 'pointOfContact'
        if contact.get('role', None) is not None:
            role_str = contact.get('role')
        role.set("codeListValue", role_str)

    def _write_keywords(self, keywords):
        """
        Generate XML mri:MD_Keywords construct

        :param keywords: keywords CSV string
        :returns: XML as etree.Element
        """
        md_keywords = etree.Element(util.nspath_eval('mri:MD_Keywords', self.namespaces))
        for kw in keywords.split(','):
            keyword = etree.SubElement(md_keywords, util.nspath_eval('mri:keyword', self.namespaces))
            etree.SubElement(keyword, util.nspath_eval('gco:CharacterString', self.namespaces)).text = kw
        return md_keywords

    def _write_extent(self, bbox, vert_ext_min, vert_ext_max):
        """
        Generate XML for a bounding box in 2 dimensions
        or a bounding box and vertical extent in 3 dimensions

        :param bbox: bounding box in EWKT (Extended Well Known Text) format
        :param vert_ext_min: vertical extent minimum, pass in None for 2D
        :param vert_extent_max: vertical extent maximum, pass in None for 2D
        :returns: XML as etree.Element
        """
        if bbox is not None:
            try:
                bbox2 = util.wkt2geom(bbox)
            except:
                return None
            extent = etree.Element(util.nspath_eval('mri:extent', self.namespaces))
            ex_extent = etree.SubElement(extent, util.nspath_eval('gex:EX_Extent', self.namespaces))
            gbb = build_path(ex_extent, ['gex:geographicElement', 'gex:EX_GeographicBoundingBox'], self.namespaces)
            west = etree.SubElement(gbb, util.nspath_eval('gex:westBoundLongitude', self.namespaces))
            east = etree.SubElement(gbb, util.nspath_eval('gex:eastBoundLongitude', self.namespaces))
            south = etree.SubElement(gbb, util.nspath_eval('gex:southBoundLatitude', self.namespaces))
            north = etree.SubElement(gbb, util.nspath_eval('gex:northBoundLatitude', self.namespaces))

            etree.SubElement(west, util.nspath_eval('gco:Decimal', self.namespaces)).text = str(bbox2[0])
            etree.SubElement(south, util.nspath_eval('gco:Decimal', self.namespaces)).text = str(bbox2[1])
            etree.SubElement(east, util.nspath_eval('gco:Decimal', self.namespaces)).text = str(bbox2[2])
            etree.SubElement(north, util.nspath_eval('gco:Decimal', self.namespaces)).text = str(bbox2[3])

            # If there is a vertical extent
            if vert_ext_min is not None and vert_ext_max is not None:
                vert_ext = build_path(ex_extent, ['gex:verticalElement', 'gex:EX_VerticalExtent'], self.namespaces)
                min_val = build_path(vert_ext, ['gex:minimumValue', 'gco:Real'], self.namespaces)
                min_val.text = vert_ext_min
                max_val = build_path(vert_ext, ['gex:maximumValue', 'gco:Real'], self.namespaces)
                max_val.text = vert_ext_max

            return extent
        return None

    # new functions
    def _write_string(self, node: Element, path: list, value: str):
        """Write out a single XML string literal Element at the end of a path of XML Elements it will create

        :param node: XML element to attach to
        :param path: the hierarchy of XML element names (prefixed form) that will be created
        :param value: string literal value
        :returns: None, but writes the new XML back to the given node"""
        etree.SubElement(
            build_path(node, path, self.namespaces),
            util.nspath_eval('gco:CharacterString', self.namespaces)
        ).text = value

    def _write_code(self, node: Element, path: list, codelist_iri: str, value: str):
        """Write out a single XML codelist Element at the end of a path of XML Elements it will create.

        This function will assign the given value to both an attribute of code= and to the text value of the XML Element
        made from the codelist_iri parameter.

        :param node: XML element to attach to
        :param path: the hierarchy of XML element names (prefixed form) that will be created
        :param codelist_iri: the codelist IRI in prefixed form
        :param value: the codelist value as a string
        :returns: None, but writes the new XML back to the given node"""
        etree.SubElement(
            build_path(node, path, self.namespaces),
            util.nspath_eval(codelist_iri, self.namespaces),
            codeList=f'{CODELIST}#{codelist_iri.split(":")[1]}',
            codeListValue=value
        ).text = value

    def _write_date(self, node: Element, property: str, date_type: str, value: str):
        """Write out a single data value within a cit:CI_Date > cit:date > gco:Date|gco:DateTime and
        cit:CI_Date > cit:dateType Element hierarchy

        :param node: XML element to attach to
        :param property: the XML Element property linking the CI_Date object this function will create to the node
        :param date_type: the date type code value from CI_DateTypeCode - a role this date plays with respect to its parent node
        :param value: data value as a string
        """

        # handle known bad date formats like 30/03/1983 - should be 1983-03-30
        # TODO: remote this if source dates are known to be be good
        def return_good_or_fix_bad_date(date_text):
            if "/" in date_text:
                try:
                    return datetime.strftime(datetime.strptime(date_text, '%d/%m/%Y'), '%Y-%m-%d')
                except ValueError:
                    pass

            return date_text

        d = build_path(node, [property, 'cit:CI_Date'], self.namespaces, reuse=False)
        etree.SubElement(
            build_path(d, ['cit:date'], self.namespaces),
            util.nspath_eval('gco:DateTime' if 'T' in value else 'gco:Date', self.namespaces),
        ).text = return_good_or_fix_bad_date(value)
        self._write_code(d, ['cit:dateType'], 'cit:CI_DateTypeCode', date_type)

    # TODO: replace static information with dynamic
    def _write_party_org_gssa(self, ci_resp):
        """Temporary function delivering static GSSA organisation party metadata. To be replaced with dynamic lookup
        information"""
        org = build_path(ci_resp, ['cit:party', 'cit:CI_Organisation'], self.namespaces)
        self._write_string(org, ['cit:name'], 'Geological Survey of South Australia')

        contact_info = build_path(org, ['cit:contactInfo', 'cit:CI_Contact'], self.namespaces)
        telephone = build_path(contact_info, ['cit:phone', 'cit:CI_Telephone'], self.namespaces)
        self._write_string(telephone, ['cit:number'], '+61 8 8463 3000')
        self._write_code(telephone, ['cit:numberType'], 'cit:CI_TelephoneTypeCode', 'voice')

        address = build_path(contact_info, ['cit:address', 'cit:CI_Address'], self.namespaces)
        self._write_string(address, ['cit:deliveryPoint'], 'Level 4, 11 Waymouth Street Adelaide, South Australia 5000')
        self._write_string(address, ['cit:city'], 'Adelaide')
        self._write_string(address, ['cit:administrativeArea'], 'South Australia')
        self._write_string(address, ['cit:postalCode'], '5000')
        self._write_string(address, ['cit:country'], 'Australia')
        self._write_string(address, ['cit:electronicMailAddress'], 'dem.media@sa.gov.au')

    # TODO: replace static information with dynamic
    def _write_party_point_of_contact(self, ci_resp):
        """Temporary function delivering static GSSA individual party metadata. To be replaced with dynamic lookup
        information"""
        person = build_path(ci_resp, ['cit:party', 'cit:CI_Individual'], self.namespaces, reuse=False)
        self._write_string(person, ['cit:name'], 'Geological Survey of South Australia')
        self._write_string(person, ['cit:positionName'], 'SARIG Customer Support')
# END of class


def get_resource_opname(operations):
    """
    Looks for resource opename in a CSV string

    :param operations: CSV string of operations
    :returns: operation name
    """
    for op in operations.split(','):
        if op in ['GetMap', 'GetFeature', 'GetCoverage', 'GetObservation']:
            return op
    return None


def build_path(node, path_list, nsmap, reuse=True):
    """
    Generic routine to build an etree.Element path
    Set reuse=False if you want to create duplicates

    :param node: add elements to this Element
    :param path_list: list of xml tags of new path to create, list of strings
    :param reuse: if False will always create new Elements along this path
    :return: returns the last etree.Element in the new Element path
    """
    tail = node
    for elem_name in path_list:
        # Does the next node in the path exist?
        next_node = node.find(elem_name, namespaces=nsmap)
        # If next node does not exist or reuse flag is False then create it
        if next_node is None or not reuse:
            tail = etree.SubElement(tail, util.nspath_eval(elem_name, nsmap))
        else:
            tail = next_node
    return tail
