# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import cache_pb2 as cache__pb2


class CacheServiceStub(object):
    """Definición del servicio de caché
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetCharacterById = channel.unary_unary(
                '/CacheService/GetCharacterById',
                request_serializer=cache__pb2.CharacterRequest.SerializeToString,
                response_deserializer=cache__pb2.CharacterResponse.FromString,
                )


class CacheServiceServicer(object):
    """Definición del servicio de caché
    """

    def GetCharacterById(self, request, context):
        """Método para obtener un personaje por su ID
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CacheServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetCharacterById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCharacterById,
                    request_deserializer=cache__pb2.CharacterRequest.FromString,
                    response_serializer=cache__pb2.CharacterResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'CacheService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CacheService(object):
    """Definición del servicio de caché
    """

    @staticmethod
    def GetCharacterById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CacheService/GetCharacterById',
            cache__pb2.CharacterRequest.SerializeToString,
            cache__pb2.CharacterResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
