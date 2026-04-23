
import hashlib
import datetime

class SistemaLogistica:
    def __init__(self,clave:str):
        self._sistemaSeguridad = Configuracion(clave)
        self._listaDespachos = []
        self._listaTransportes = []
    def calcularSumatoriaPesos(self,desde :datetime,hasta:datetime):
        return sum(despacho.getPesoEnRango(desde,hasta) for despacho in self._listaDespachos)

    def despachar(self, clave: str, carga: list[Contenedor], transporte: Transporte):
        if self._sistemaSeguridad.validarClave(clave):
            despacho=Despacho(datetime.date.today(), "DESPACHADO")
            for contenedor in carga:
                despacho.agregarContenedor(contenedor)
            despacho.asignarTransporte(transporte)
            self._listaDespachos.append(despacho)
            print("[PEDIDO DESPACHADO]")
            print(f"Identidad del Transporte (ID: {transporte.getID()}): {transporte} {transporte.getPatente()}")
            print(f"Estado:  {despacho.getEstado()}  exitosamente." )
            print(f"Carga total:  {despacho.getPesoTotal()} kg.")
            print("Verificación de Seguridad: Hash SHA256 Validado.")
            print("-----------------------------------------------------")
            print("Detalle de la Carga: ")
            despacho.getInfo()
        else:
            print("HASH EQUIVOCADO")


class Configuracion:
    def __init__(self,clave):
        self._hashClave = hashlib.sha256(clave.encode()).hexdigest()

    def validarClave(self, clave : str):
        BOOLEANO=False
        if hashlib.sha256(clave.encode()).hexdigest() == self._hashClave:
            BOOLEANO=True
        return BOOLEANO


class Despacho:
    def __init__(self,fechaDespacho : datetime, estado : str):
        self.fechaDespacho=fechaDespacho
        self.estado=estado
        self.listaContenedores=[]
        self.transporteAsignado=None

    def agregarContenedor(self, contenedor : Contenedor):
        self.listaContenedores.append(contenedor)
    
    def getPesoTotal(self):
        return sum(contenedor.getPesoTotal() for contenedor in self.listaContenedores)
    
    def getPesoEnRango(self, desde, hasta):
        return self.getPesoTotal() if desde<=self.fechaDespacho<=hasta else 0
    
    def asignarTransporte(self,transporte : Transporte):
        self.transporteAsignado=transporte

    def getInfo(self):
        i=0
        for contenedor in self.listaContenedores:
            i+=1
            print(f"-  Contenedor {i} (Peso:  {contenedor.getPesoTotal()} kg), contiene:")
            contenedor.getInfo()
    def getEstado(self):
        return self.estado


class Contenedor:
    def __init__(self):
        self.paquetes= []
    def agregarpaquete(self, paquete:Paquete):
        self.paquetes.append(paquete)
    def getPesoTotal(self):
        return sum(paquete.getPeso() for paquete in self.paquetes)
    def getInfo(self):
        i=0
        for paquete in self.paquetes:
            i+=1
            print(f"* Paquete {i} ( {paquete.getPeso()} kg)")


class Paquete:
    def __init__(self, peso : float):
        self.peso=peso
    def getPeso(self):
        return self.peso


class Transporte():
    def __init__(self, nroID : int, patente : str):
        self.nroID=nroID
        self.patente=patente
    
    def getPatente(self):
        return self.patente 
   
    def getID(self):
        return self.nroID


class Camion(Transporte):
    def __init__(self, capacidadKG : float, patente, nroID):
        super().__init__(nroID,patente)
        self.capacidadKG=capacidadKG
    def __str__(self):
        return "Camion"
 

class Avion(Transporte):
    def __init__(self,tiempoVuelo : float,nroID,patente):
        super().__init__(nroID,patente)
        self.tiempoVuelo=tiempoVuelo
    def __str__(self):
        return "Avion"


if __name__ == "__main__":

    sistema = SistemaLogistica("logistica123")
    avion = Avion(5.0, 1402345678, "LV-X500")

    contA = Contenedor()
    contA.agregarpaquete(Paquete(50))
    contA.agregarpaquete(Paquete(50))

    contB = Contenedor()
    contB.agregarpaquete(Paquete(120))

    carga = [contA, contB]

    sistema.despachar("logistica123", carga, avion)