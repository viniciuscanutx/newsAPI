from typing import Literal, Enum

FeedCategory = Literal["tech", "negocios", "cultura", "esportes", "politica", "internacional", "ciencia", "saude", "educacao", "economia", "financas", "carreira", "relacionamento", "familia", "viagem", "gastronomia", "moda", "beleza", "automotivo", "tecnologia", "entretenimento", "saude", "educacao", "economia", "financas", "carreira", "relacionamento", "familia", "viagem", "gastronomia", "moda", "beleza", "automotivo"]

class FeedCategory(str, Enum):
    TECH = "tech"
    NEGOCIOS = "negocios"
    CULTURA = "cultura"
    ESPORTES = "esportes"
    POLITICA = "politica"
    INTERNACIONAL = "internacional"
    CIENCIA = "ciencia"
    SAUDE = "saude"
    EDUCACAO = "educacao"
    ECONOMIA = "economia"
    FINANCAS = "financas"
    CARREIRA = "carreira"
    RELACIONAMENTO = "relacionamento"
    FAMILIA = "familia"
    VIAGEM = "viagem"
    GASTRONOMIA = "gastronomia"
    MODA = "moda"
    BELEZA = "beleza"
    AUTOMOTIVO = "automotivo"