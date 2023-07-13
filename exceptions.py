class NoHayInformacionParaPersistir(Exception):
    """ Excepción que se lanza cuando no hay informacion para persistir"""

class NombreDeArchivoYaExistente(Exception):
    """ Excepción que se lanza cuando el nombre elegido para persiste ya existe """

class UsuarioNoExisteEnLaInformacionRecuperada(Exception):
    """ Excepción que se lanza cuando el usuario ingresado no existe en la informacion que se recupero"""