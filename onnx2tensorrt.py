import onnx
#import backend
import numpy as np
import os 
import timeit
import pycuda.driver as cuda
import pycuda.autoinit
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
import tensorrt as trt
TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
#ONNX_MODEL = "mnist.onnx"
ONNX_MODEL = "Bisenet.onnx"
def build_engine():
    with trt.Builder(TRT_LOGGER) as builder, builder.create_network() as network, trt.OnnxParser(network, TRT_LOGGER) as parser:
        # Configure the builder here.
        
        # Parse the model to create a network.
        with open(ONNX_MODEL, 'rb') as model:
            parser.parse(model.read())
        builder.max_workspace_size = 2**30 
        network.mark_output(network.get_layer(network.num_layers - 1).get_output(0))
        #engine = builder.build_cuda_engine(network)
              
        with builder.build_cuda_engine(network) as engine:
            #serialized_engine = engine.serialize()
            #with open("sample.engine", "wb") as f:
                #f.write(engine.serialize())
            #with trt.Runtime(TRT_LOGGER) as runtime:
                #engine = runtime.deserialize_cuda_engine(serialized_engine)
                
            with open("sample.engine", "rb") as f, trt.Runtime(TRT_LOGGER) as runtime:
                engine = runtime.deserialize_cuda_engine(f.read())
            #context = engine.create_execution_context()
                #start_time = timeit.default_timer()
                input_data = np.random.random(size=(16, 3, 640, 480)).astype(np.float32)
            #d_input = cuda.mem_alloc(input_data.nbytes)
            #d_output = cuda.mem_alloc()
            #bindings = [int(d_input),int(d_output)]
            #stream = cuda.Stream()
            #context.enqueue(batch_size,bindings,stream.handle,None)
            #cuda.memcpy_dtoh_async(output,d_output,stream)
            #print(output)
                
            #input_data = np.random.random(size=(32, 3, 640, 480)).astype(np.float32)
            #output_data = engine.run(input_data)[0]
            #print(output_data)
            #print(output_data.shape)
                h_input = cuda.pagelocked_empty(input_data.shape, dtype=np.float32)
                h_output = cuda.pagelocked_empty(input_data.shape, dtype=np.float32)
                d_input = cuda.mem_alloc(input_data.nbytes)
                d_output = cuda.mem_alloc(input_data.nbytes)
                stream = cuda.Stream()
                start_time = timeit.default_timer()
                with engine.create_execution_context() as context:
                    cuda.memcpy_htod_async(d_input, h_input, stream)
                    context.execute_async(bindings=[int(d_input), int(d_output)], stream_handle=stream.handle)
                    cuda.memcpy_dtoh_async(h_output, d_output, stream)
                    stream.synchronize() 
                    print(h_output)
                end_time = timeit.default_timer()  
                print("the time of tensorrt inference is %s" % (end_time - start_time))
                return h_output  

        # Build and return the engine. Note that the builder, network and parser are destroyed when this function returns.
        #return builder.build_cuda_engine(network)
#model = onnx.load("./Bisenet.onnx")
#engine = backend.prepare(model, device='CUDA:0')
#input_data = np.random.random(size=(32, 3, 640, 480)).astype(np.float32)
#output_data = engine.run(input_data)[0]
#print(output_data)
#print(output_data.shape)
#start_time = timeit.default_timer()
build_engine()
#end_time = timeit.default_timer()
#print("the time of tensorrt inference is %s" % (end_time - start_time))



    
