from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter
from rasa_nlu.components import ComponentBuilder
import yaml
import io


builder = ComponentBuilder(use_cache=True)

def read_file(filename, encoding="utf-8-sig"):
    """Read text from a file."""
    with io.open(filename, encoding=encoding) as f:
        return f.read()

def fix_yaml_loader():
    """Ensure that any string read by yaml is represented as unicode."""
    from yaml import Loader, SafeLoader

    def construct_yaml_str(self, node):
        # Override the default string handling function
        # to always return unicode objects
        return self.construct_scalar(node)

    Loader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)
    SafeLoader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)


def read_yaml(content):
    fix_yaml_loader()
    return yaml.load(content)


def read_yaml_file(filename):
    fix_yaml_loader()
    return yaml.load(read_file(filename, "utf-8"))

def train_nlu(data, config, model_dir):
    training_data = load_data(data)
    trainer = Trainer(RasaNLUModelConfig(config))
    trainer.train(training_data)
    model_directory = trainer.persist(model_dir, fixed_model_name='activesgfaqnlu')


def run_nlu():
    interpreter = Interpreter.load('./models/nlu/default/activesgfaqnlu', component_builder=None)
    print(interpreter.parse(u"what is activesg"))


if __name__ == '__main__':
    #train_nlu('./data/data.json', read_yaml_file('config_spacy.yml'), './models/nlu')
    run_nlu()