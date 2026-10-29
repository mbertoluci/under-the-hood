# A regra que qualquer pessoa escreveria: nega se a carga não está liberada.
package ingenua

import rego.v1

nega contains "a carga não está liberada" if input.carga.status != "liberada"

default permitido := false

permitido if count(nega) == 0
