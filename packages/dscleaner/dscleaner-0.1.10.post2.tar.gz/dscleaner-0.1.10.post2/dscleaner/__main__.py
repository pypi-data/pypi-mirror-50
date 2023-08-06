import click
class Number(click.ParamType):
    name = "Numeric"
    def convert(self, value, param, ctx):
        try:
            if("." in value):
                return float(value)
            else:
                return int(value)
        except (TypeError,ValueError):
            self.fail(
                "Expected an int or float value, got "
                f"{value!r} of type {type(value).__name__}",
                param,
                ctx,
            )

@click.command()
@click.argument(
    'input',
    type=click.Path(exists=True,resolve_path=True),
)
@click.argument(
    'output',
    type=click.Path(file_okay=False,dir_okay=False,resolve_path=True),
)
@click.option(
    '--resample',
    '-r',
    help='Value the dataset must be resampled to',
    type=click.INT,
)
@click.option(
    '--fix_duration',
    '-f',
    help='Duration in minutes every dataset file should have.',
    type=Number()
)
@click.option(
    '--natsort/--no-natsort',
    default=True,
    help='Whether the folder contents should be crescently natural sorted or not',
)
def cli(resample,fix_duration,input,output,natsort):
    #it also should normalize but in order to do that it must accept an array of values...
    import os

    from .utils import is_number   
    if(resample is not None):
        if(not is_number(resample)):
            print("Invalid resample value!")
            return
        resample= float(resample)

    if(fix_duration is not None):
        if(not is_number(fix_duration)):
            print("Invalid fix_duration value!")
        fix_duration = float(fix_duration)

    from .fileinfo import FileInfo
    from .fileutil import FileUtil
        
    if(os.path.isdir(input) or '*' in input):
        #print(">pasta")
        from .merger import Merger
        from .utils import path_splitter
        files = os.listdir(input)
        if(natsort):
            import natsort as nat
            files = nat.natsorted(files, key = lambda y: y.lower()) #orders crescently
        with click.progressbar(files, label = 'Processing dataset...') as bar:
            for f in bar:
                name = path_splitter(input+'/'+f)['full_path']
                try:
                    with FileInfo(name) as file:
                        with FileUtil(file) as futil:
                            if(fix_duration):
                                futil.fix_duration(fix_duration)
                            if(resample):
                                val = resample
                                futil.resample(resample)
                            else:
                                val = file.getSamplerate()
                        with Merger(file.getNumberOfChannels(),output,int(val)) as fw:
                            fw.add(file)
                            fw.create_file()
                except RuntimeError:
                    pass
    else:

        #print(">ficheiro")     

        from .filewriter import FileWriter
        with click.progressbar(length=3,label = "Converting file") as bar:
            bar.update(1)
            with FileInfo(input) as file:
                with FileUtil(file) as futil:
                    if(fix_duration):
                        futil.fix_duration(fix_duration)
                    if(resample):
                        futil.resample(resample)
                    bar.update(2)
                with FileWriter(file) as fw:
                    fw.create_file(output)
                bar.update(3)

cli()