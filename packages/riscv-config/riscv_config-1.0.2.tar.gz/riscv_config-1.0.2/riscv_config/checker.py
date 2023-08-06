import os
import logging

from cerberus import Validator

import riscv_config.utils as utils
from riscv_config.errors import ValidationError
from riscv_config.schemaValidator import schemaValidator
import riscv_config.constants as constants
from riscv_config.utils import yaml

logger = logging.getLogger(__name__)

def iset():
    '''Function to check and set defaults for all "implemented" fields which are dependent on 
        the xlen.'''
    global inp_yaml
    if '32' in inp_yaml['ISA']:
        return False
    else:
        return True


def nosset():
    '''Function to check and set defaults for all fields which are dependent on 
        the presence of 'S' extension and have a hardwired value of 0.'''
    global inp_yaml
    if 'S' not in inp_yaml['ISA']:
        return {'is_hardwired': True, 'hardwired_val': 0}
    else:
        return {'is_hardwired': False}


def nouset():
    '''Function to check and set defaults for all fields which are dependent on 
        the presence of 'U' extension and have a hardwired value of 0.'''
    global inp_yaml
    if 'U' not in inp_yaml['ISA']:
        return {'is_hardwired': True, 'hardwired_val': 0}
    else:
        return {'is_hardwired': False}


def upieset(doc):
    '''Function to check and set value for upie field in misa.'''
    global inp_yaml
    if 'U' not in inp_yaml['ISA']:
        return {'is_hardwired': True, 'hardwired_val': 0}
    elif 'UPIE' not in doc.keys():
        return {'is_hardwired': False}
    else:
        return doc['UPIE']


def uieset(doc):
    '''Function to check and set value for uie field in misa.'''
    global inp_yaml
    if 'U' not in inp_yaml['ISA']:
        return {'is_hardwired': True, 'hardwired_val': 0}
    elif 'UIE' not in doc.keys():
        return {'is_hardwired': False}
    else:
        return doc['UIE']


def twset():
    '''Function to check and set value for tw field in misa.'''
    global inp_yaml
    if 'S' not in inp_yaml['ISA'] and 'U' not in inp_yaml['ISA']:
        return {'is_hardwired': True, 'hardwired_val': 0}
    else:
        return {'is_hardwired': False}


def miedelegset():
    '''Function to set "implemented" value for mideleg regisrer.'''
    # return True
    global inp_yaml
    if 'U' not in inp_yaml['ISA']:
        return False
    elif (('U' in inp_yaml['ISA']) and
          not ('N' in inp_yaml['ISA'] or 'S' in inp_yaml['ISA'])):
        return False
    else:
        return True


def mepcset():
    return {
        'range': {
            'rangelist': [[0, int("FFFFFFFF", 16)]],
            'mode': "Unchanged"
        }
    }


def xtvecset():
    return {
        'BASE': {
            'range': {
                'rangelist': [[0, int("3FFFFFFF", 16)]],
                'mode': "Unchanged"
            }
        },
        'MODE': {
            'range': {
                'rangelist': [[0]],
                'mode': "Unchanged"
            }
        }
    }


def simpset():
    global inp_yaml
    if 'S' in inp_yaml['ISA']:
        return True
    else:
        return False


def satpset():
    return {'MODE': {'range': {'rangelist': [[0]]}}}


def findxlen():
    global inp_yaml
    if "32" in inp_yaml['ISA']:
        xlen = 32
    elif "64" in inp_yaml['ISA']:
        xlen = 64
    elif "128" in inp_yaml['ISA']:
        xlen = 128
    return xlen


def xlenset():
    return findxlen()


def add_def_setters(schema_yaml):
    '''Function to set the default setters for various fields in the schema'''
    schema_yaml['mstatus']['schema']['SXL']['schema']['implemented'][
        'default_setter'] = lambda doc: iset()
    schema_yaml['mstatus']['schema']['UXL']['schema']['implemented'][
        'default_setter'] = lambda doc: iset()
    schema_yaml['mstatus']['schema']['TVM'][
        'default_setter'] = lambda doc: nosset()
    schema_yaml['mstatus']['schema']['TSR'][
        'default_setter'] = lambda doc: nosset()
    schema_yaml['mstatus']['schema']['MXR'][
        'default_setter'] = lambda doc: nosset()
    schema_yaml['mstatus']['schema']['SUM'][
        'default_setter'] = lambda doc: nosset()
    schema_yaml['mstatus']['schema']['SPP'][
        'default_setter'] = lambda doc: nosset()
    schema_yaml['mstatus']['schema']['SPIE'][
        'default_setter'] = lambda doc: nosset()
    schema_yaml['mstatus']['schema']['SIE'][
        'default_setter'] = lambda doc: nosset()
    schema_yaml['mstatus']['schema']['UPIE'][
        'default_setter'] = lambda doc: upieset(doc)
    schema_yaml['mstatus']['schema']['UIE'][
        'default_setter'] = lambda doc: uieset(doc)
    schema_yaml['mstatus']['schema']['MPRV'][
        'default_setter'] = lambda doc: nouset()
    schema_yaml['mstatus']['schema']['TW'][
        'default_setter'] = lambda doc: twset()
    schema_yaml['mideleg']['schema']['implemented'][
        'default_setter'] = lambda doc: miedelegset()
    schema_yaml['medeleg']['schema']['implemented'][
        'default_setter'] = lambda doc: miedelegset()
    schema_yaml['mepc']['default_setter'] = lambda doc: mepcset()
    schema_yaml['mtvec']['default_setter'] = lambda doc: xtvecset()
    schema_yaml['stvec']['default_setter'] = lambda doc: xtvecset()
    schema_yaml['satp']['default_setter'] = lambda doc: satpset()
    schema_yaml['stvec']['schema']['implemented'][
        'default_setter'] = lambda doc: simpset()
    schema_yaml['sie']['schema']['implemented'][
        'default_setter'] = lambda doc: simpset()
    schema_yaml['sip']['schema']['implemented'][
        'default_setter'] = lambda doc: simpset()
    schema_yaml['scounteren']['schema']['implemented'][
        'default_setter'] = lambda doc: simpset()
    schema_yaml['sepc']['schema']['implemented'][
        'default_setter'] = lambda doc: simpset()
    schema_yaml['satp']['schema']['implemented'][
        'default_setter'] = lambda doc: simpset()
    schema_yaml['xlen']['default_setter'] = lambda doc: xlenset()
    return schema_yaml


def imp_normalise(foo):
    '''
        Function to trim the dictionary. Any node with implemented field set to false is trimmed of all the other nodes.
        
        :param foo: The dictionary to be trimmed.
        
        :type foo: dict

        :return: The trimmed dictionary.
    '''
    for key in foo.keys():
        if isinstance(foo[key], dict):
            foo[key] = imp_normalise(foo[key])
        if key == 'implemented':
            if not foo[key]:
                foo = {'implemented': False}
                break
    return foo

def check_specs(isa_spec, platform_spec, work_dir,logging=False):
    ''' 
        Function to perform ensure that the isa and platform specifications confirm
        to their schemas. The :py:mod:`Cerberus` module is used to validate that the
        specifications confirm to their respective schemas.

        :param isa_spec: The path to the DUT isa specification yaml file. 

        :param platform_spec: The path to the DUT platform specification yaml file.

        :param logging: A boolean to indicate whether log is to be printed.

        :type logging: bool
        
        :type isa_spec: str

        :type platform_spec: str

        :raise ValidationError: It is raised when the specifications violate the 
            schema rules. It also contains the specific errors in each of the fields.
        
        :return: A tuple with the first entry being the absolute path to normalized isa file 
            and the second being the absolute path to the platform spec file.
    '''
    global inp_yaml

    if logging:
        logger.info('Input-ISA file')

    foo = isa_spec
    schema = constants.isa_schema
    """
      Read the input-isa foo (yaml file) and validate with schema-isa for feature values
      and constraints
    """
    # Load input YAML file
    if logging:
        logger.info('Loading input file: ' + str(foo))
    inp_yaml = utils.load_yaml(foo)

    # instantiate validator
    if logging:
        logger.info('Load Schema ' + str(schema))
    schema_yaml = utils.load_yaml(schema)

    #Extract xlen
    xlen = findxlen()

    schema_yaml = add_def_setters(schema_yaml)
    validator = schemaValidator(schema_yaml, xlen=xlen)
    validator.allow_unknown = False
    validator.purge_readonly = True
    normalized = validator.normalized(inp_yaml, schema_yaml)

    # Perform Validation
    if logging:
        logger.info('Initiating Validation')
    valid = validator.validate(inp_yaml)

    # Print out errors
    if valid:
        if logging:
            logger.info('No Syntax errors in Input ISA Yaml. :)')
    else:
        error_list = validator.errors
        raise ValidationError("Error in " + foo + ".",error_list)

    file_name = os.path.split(foo)
    file_name_split = file_name[1].split('.')
    output_filename = os.path.join(
        work_dir, file_name_split[0] + '_checked.' + file_name_split[1])
    ifile = output_filename
    outfile = open(output_filename, 'w')
    if logging:
        logger.info('Dumping out Normalized Checked YAML: ' + output_filename)
    yaml.dump(imp_normalise(normalized), outfile)

    if logging:
        logger.info('Input-Platform file')

    foo = platform_spec
    schema = constants.platform_schema
    """
      Read the input-platform foo (yaml file) and validate with schema-platform for feature values
      and constraints
    """
    # Load input YAML file
    if logging:
        logger.info('Loading input file: ' + str(foo))
    inp_yaml = utils.load_yaml(foo)
    if inp_yaml is None:
        inp_yaml = {'mtime': {'implemented': False}}

    # instantiate validator
    if logging:
        logger.info('Load Schema ' + str(schema))
    schema_yaml = utils.load_yaml(schema)

    validator = schemaValidator(schema_yaml, xlen=xlen)
    validator.allow_unknown = False
    validator.purge_readonly = True
    normalized = validator.normalized(inp_yaml, schema_yaml)

    # Perform Validation
    if logging:
        logger.info('Initiating Validation')
    valid = validator.validate(inp_yaml)

    # Print out errors
    if valid:
        if logging:
            logger.info('No Syntax errors in Input Platform Yaml. :)')
    else:
        error_list = validator.errors
        raise ValidationError("Error in " + foo + ".",error_list)

    file_name = os.path.split(foo)
    file_name_split = file_name[1].split('.')
    output_filename = os.path.join(
        work_dir, file_name_split[0] + '_checked.' + file_name_split[1])
    pfile = output_filename
    outfile = open(output_filename, 'w')
    if logging:
        logger.info('Dumping out Normalized Checked YAML: ' + output_filename)
    yaml.dump(imp_normalise(normalized), outfile)
    return (ifile, pfile)
