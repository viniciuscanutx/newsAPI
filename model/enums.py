from enum import Enum


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