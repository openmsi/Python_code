#imports
from .config_file_parser import ConfigFileParser
from .serialization import DataFileChunkSerializer
from confluent_kafka import Producer, SerializingProducer
from confluent_kafka.serialization import DoubleSerializer, IntegerSerializer, StringSerializer

class MyProducer(Producer) :
    """
    Class to extend Kafka Producers for specific scenarios
    """

    def __init__(self,config_dict) :
        super().__init__(config_dict)

    @classmethod
    def from_file(cls,config_file_path,**kwargs) :
        """
        config_file_path = path to the config file to use in defining this producer

        Possible keyword arguments:
        logger = the logger object to use
        !!!!! any other keyword arguments will be added to the configuration (with underscores replaced with dots) !!!!!
        """
        parser = ConfigFileParser(config_file_path,**kwargs)
        configs = parser.get_config_dict_for_groups(['cluster','producer'])
        for argname,arg in kwargs.items() :
            if argname=='logger' :
                continue
            configs[argname.replace('_','.')]=arg
        return cls(configs)

class MySerializingProducer(SerializingProducer) :
    """
    Class to extend Kafka SerializingProducers for specific scenarios
    """

    def __init__(self,config_dict) :
        super().__init__(config_dict)

    @classmethod
    def from_file(cls,config_file_path,**kwargs) :
        """
        config_file_path = path to the config file to use in defining this producer

        Possible keyword arguments:
        logger = the logger object to use
        !!!!! any other keyword arguments will be added to the configuration (with underscores replaced with dots) !!!!!
        """
        parser = ConfigFileParser(config_file_path,**kwargs)
        configs = parser.get_config_dict_for_groups(['cluster','producer'])
        for argname,arg in kwargs.items() :
            if argname=='logger' :
                continue
            configs[argname.replace('_','.')]=arg
        #if one of several recognized serializers have been given as config paramenters for the key/value serializer, replace them with the actual class
        names_to_classes = {
            'DoubleSerializer': DoubleSerializer(),
            'IntegerSerializer': IntegerSerializer(),
            'StringSerializer': StringSerializer(),
            'DataFileChunkSerializer': DataFileChunkSerializer(),
        }
        configs_to_check = ['key.serializer','value.serializer']
        for cfg in configs_to_check :
            if cfg in configs.keys() :
                if configs[cfg] in names_to_classes :
                    configs[cfg] = names_to_classes[configs[cfg]]
        return cls(configs)
