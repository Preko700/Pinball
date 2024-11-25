class CircuitoMenos3:
    def __init__(self):
        self.habilitado = False

    def habilitar(self):
        self.habilitado = True

    def deshabilitar(self):
        self.habilitado = False

    def restar_3(self, bits):
        if not self.habilitado:
            return bits

        # Convertir los bits a un número entero
        numero = int(bits, 2)

        # Restar 3 de manera circular
        resultado = (numero - 3) % 8

        # Convertir el resultado de nuevo a bits
        resultado_bits = format(resultado, '03b')

        return resultado_bits

    def procesar_puntaje(self, puntaje):
        # Obtener el dígito más significativo
        digito_mas_significativo = int(str(puntaje)[0])

        # Convertir el dígito a binario
        binario = format(digito_mas_significativo, '04b')

        # Tomar los 3 bits menos significativos
        bits_menos_significativos = binario[-3:]

        # Restar 3 de manera circular
        resultado_bits = self.restar_3(bits_menos_significativos)

        return resultado_bits