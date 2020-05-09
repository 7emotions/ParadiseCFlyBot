import configparser
import json

ini_file_path = './../conf/conf.ini'


def getAdminQid() :
    '''
    get HA Qid from .ini file
    '''
    con = configparser.ConfigParser()
    con.read(ini_file_path)
    qid_list = con.get('Admin_qid','qid')
    qid_list = json.loads(qid_list)

    return qid_list

def getHAQid() :
    '''
    get HA Qid from .ini file
    '''
    con = configparser.ConfigParser()
    con.read(ini_file_path)
    qid_list = con.get('HA_qid','qid')
    qid_list = json.loads(qid_list)

    return qid_list

def addHAQid( qid ) :
    '''
    add a qid to .ini file
    '''
    con = configparser.ConfigParser()
    con.read(ini_file_path)
    qid_list = getHAQid()
    qid_list.append(int(qid))

    try :
        con.set('HA_qid','qid',repr(qid_list))
        with open(ini_file_path,'w') as fileObj :
            con.write(fileObj)
        return True
    except configparser.DuplicateSectionError :
        return False
