from .pyads import ADS


## Note: Nothing here is tested yet!
def add_data_to_stream(file_source, stream_name, stream_data):
    handler = ADS(file_source)
    handler.add_stream_from_string(stream_name, stream_data)

def list_streams_from_file(file_source):
    handler = ADS(file_source)
    if handler.has_streams():
        for stream in handler.streams[:]:
            print(file_source + ":" + stream)
            
def extract_streams_from_file(file_source):
    handler = ADS(file_source)
    if handler.has_streams():
        for stream in handler.streams[:]:
            print(file_source + ":" + stream)
            with open(stream, 'wb') as f:
                f.write(handler.get_stream_content(stream))

def remove_streams_from_file(file_source):
    handler = ADS(file_source)
    if handler.has_streams():
        for stream in handler.streams[:]:
            print(file_source + ":" + stream)
            handler.streams.remove(stream)
