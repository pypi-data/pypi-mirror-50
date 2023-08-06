# -*- coding: utf-8 -*-


import pandas as pd
from slugify import slugify
from sortedcontainers.sorteddict import SortedDict
import logging


from openfisca_core.model_api import Variable, YEAR


log = logging.getLogger(__name__)


categories_fiscales_data_frame = pd.DataFrame()


def generate_postes_variables(tax_benefit_system, label_by_code_coicop):
    for code_coicop, label in label_by_code_coicop.items():
        class_name = "poste_{}".format(slugify(code_coicop, separator = '_'))
        log.info('Creating variable {} with label {}'.format(class_name, label))
        # Trick to create a class with a dynamic name.
        entity = tax_benefit_system.entities_by_singular()['household']
        tax_benefit_system.add_variable(
            type(class_name, (Variable,), dict(
                definition_period = YEAR,
                entity = entity,
                label = label,
                value_type = float,
                ))
            )


def generate_depenses_ht_postes_variables(tax_benefit_system, categories_fiscales = None, reform_key = None):
    # Almost identical to openfisca-france-indirect-taxation eponymous function
    assert categories_fiscales is not None
    assert not categories_fiscales.duplicated().any().any()
    reference_categories = sorted(categories_fiscales_data_frame['categorie_fiscale'])

    functions_by_name_by_poste = dict()
    postes_coicop_all = set()

    for categorie_fiscale in reference_categories:
        year_start = 1994
        year_final_stop = 2014
        functions_by_name = dict()
        for year in range(year_start, year_final_stop + 1):
            postes_coicop = sorted(
                categories_fiscales.query(
                    'start <= @year and stop >= @year and categorie_fiscale == @categorie_fiscale'
                    )['code_coicop'].astype(str))
            if year == year_start:
                previous_postes_coicop = postes_coicop
                continue
            if previous_postes_coicop == postes_coicop and year != year_final_stop:
                continue
            else:
                year_stop = year - 1 if year != year_final_stop else year_final_stop

                for poste_coicop in previous_postes_coicop:
                    # if not Reform:
                    dated_func = depenses_ht_postes_function_creator(
                        poste_coicop,
                        categorie_fiscale = categorie_fiscale,
                        year_start = year_start,
                        year_stop = year_stop
                        )

                    dated_function_name = "formula_{year_start}".format(
                        year_start = year_start, year_stop = year_stop)
                    log.debug('Creating fiscal category {} ({}-{}) with the following products {}'.format(
                        categorie_fiscale, year_start, year_stop, postes_coicop))

                    if poste_coicop not in functions_by_name_by_poste:
                        functions_by_name_by_poste[poste_coicop] = dict()
                    functions_by_name_by_poste[poste_coicop][dated_function_name] = dated_func

                year_start = year

            previous_postes_coicop = postes_coicop
            postes_coicop_all = set.union(set(postes_coicop), postes_coicop_all)

    assert set(functions_by_name_by_poste.keys()) == postes_coicop_all

    for poste, functions_by_name in list(functions_by_name_by_poste.items()):
        class_name = 'depenses_ht_poste_{}'.format(slugify(poste, separator = '_'))
        # if Reform is None:
        definitions_by_name = dict(
            definition_period = YEAR,
            value_type = float,
            entity = tax_benefit_system.entities_by_singular()['household'],
            label = "Dépenses hors taxe du poste_{0}".format(poste),
            )
        definitions_by_name.update(functions_by_name)
        tax_benefit_system.add_variable(
            type(class_name, (Variable,), definitions_by_name)
            )
        del definitions_by_name


def depenses_ht_postes_function_creator(poste_coicop, categorie_fiscale = None, year_start = None, year_stop = None):
    # Almost identical to openfisca-france-indirect-taxation eponymous function
    assert categorie_fiscale is not None

    def func(entity, period_arg, parameters, categorie_fiscale = categorie_fiscale):
        if (categorie_fiscale is not None) or (categorie_fiscale != ''):
            taux = parameters(period_arg.start).imposition_indirecte.tva[categorie_fiscale]
        else:
            taux = 0

        return entity('poste_' + slugify(poste_coicop, separator = '_'), period_arg) / (1 + taux)

    func.__name__ = "formula_{year_start}".format(year_start = year_start, year_stop = year_stop)
    return func


def depenses_ht_categorie_function_creator(postes_coicop, year_start = None, year_stop = None):
    if len(postes_coicop) != 0:
        def func(entity, period_arg):
            return sum(entity(
                'depenses_ht_poste_' + slugify(poste, separator = '_'), period_arg) for poste in postes_coicop
                )

        func.__name__ = "formula_{year_start}".format(year_start = year_start, year_stop = year_stop)
        return func

    else:  # To deal with Reform emptying some fiscal categories
        def func(entity, period_arg):
            return 0

    func.__name__ = "formula_{year_start}".format(year_start = year_start, year_stop = year_stop)
    return func


def generate_variables(tax_benefit_system, categories_fiscales = None, reform_key = None):
    assert categories_fiscales is not None

    completed_categories_fiscales = reference_categories = sorted(categories_fiscales_data_frame['categorie_fiscale'].drop_duplicates())

    if reform_key:
        reference_categories = set(reference_categories).union(set(categories_fiscales.categorie_fiscale.unique()))

    for categorie_fiscale in reference_categories:
        if categorie_fiscale == '':
            continue

        year_start = 1994
        year_final_stop = 2014
        functions_by_name = dict()
        formulas = SortedDict()
        for year in range(year_start, year_final_stop + 1):
            postes_coicop = sorted(
                completed_categories_fiscales.query(
                    'start <= @year and stop >= @year and categorie_fiscale == @categorie_fiscale'
                    )['code_coicop'].astype(str))

            if year == year_start:
                previous_postes_coicop = postes_coicop
                continue

            if previous_postes_coicop == postes_coicop and year != year_final_stop:
                continue
            else:
                year_stop = year - 1 if year != year_final_stop else year_final_stop

                dated_func = depenses_ht_categorie_function_creator(
                    previous_postes_coicop,
                    year_start = year_start,
                    year_stop = year_stop,
                    )
                dated_function_name = "formula_{year_start}".format(
                    year_start = year_start, year_stop = year_stop)
                log.info('Creating fiscal category {} ({}-{}) with the following products {}'.format(
                    categorie_fiscale, year_start, year_stop, previous_postes_coicop))

                functions_by_name[dated_function_name] = dated_func
                # formulas["{}-01-01".format(year_start)] = dated_func
                year_start = year

            previous_postes_coicop = postes_coicop

        class_name = 'depenses_ht_{}'.format(categorie_fiscale)

        # Trick to create a class with a dynamic name.
        if reform_key is None:
            definitions_by_name = dict(
                value_type = float,
                entity = tax_benefit_system.entities_by_singular()['household'],
                label = "Dépenses hors taxes: {0}".format(categorie_fiscale),
                )
            definitions_by_name.update(functions_by_name)
            tax_benefit_system.add_variable(
                type(class_name, (Variable,), definitions_by_name)
                )

        else:
            if class_name in tax_benefit_system.variables:
                definitions_by_name = tax_benefit_system.variables[class_name].__dict__.copy()
                definitions_by_name.update(functions_by_name)
                for attribute in ['name', 'baseline_variable', 'dtype', 'json_type', 'is_neutralized', 'formulas']:
                    definitions_by_name.pop(attribute, None)
                    # definitions_by_name['formulas'] = formulas
                tax_benefit_system.update_variable(
                    type(class_name, (Variable,), definitions_by_name)
                    )
            else:
                definitions_by_name = dict(
                    value_type = float,
                    entity = tax_benefit_system.entities_by_singular()['household'],
                    label = "Dépenses hors taxes: {0}".format(categorie_fiscale),
                    )
                definitions_by_name.update(functions_by_name)
                definitions_by_name['formulas'] = formulas
                tax_benefit_system.add_variable(
                    type(class_name, (Variable,), definitions_by_name)
                    )

        del definitions_by_name
