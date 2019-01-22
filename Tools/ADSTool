from pyads import ADS


## Note: Nothing here is tested yet!
def add_data_to_stream(file_source, stream_data):
    handler = ADS(file_source)
    handler.addStream(stream_data)

def list_streams_from_file(file_source):
    handler = ADS(file_source)
    if handler.containStreams():
        for stream in handler.getStreams()[:]:
            print(file_source + ":" + stream)
            
def extract_streams_from_file(file_source):
    handler = ADS(file_source)
    if handler.containStreams():
        for stream in handler.getStreams()[:]:
            print(file_source + ":" + stream)
            with open(stream, 'wb') as f:
                f.write(handler.getStreamContent(stream))

def remove_streams_from_file(file_source):
    handler = ADS(file_source)
    if handler.containStreams():
        for stream in handler.getStreams()[:]:
            print(file_source + ":" + stream)
            handler.removeStream(stream)
