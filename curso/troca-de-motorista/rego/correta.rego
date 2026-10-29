# Pelo lado positivo: o que libera tem default falso, e a negação usa not.
package correta

import rego.v1

default carga_liberada := false

carga_liberada if input.carga.status == "liberada"

nega contains "a carga não está liberada" if not carga_liberada

default permitido := false

permitido if count(nega) == 0
