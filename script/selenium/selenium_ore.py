#!/usr/bin/env python3
import sys
import argparse

from selenium.common import TimeoutException

import web_login
import selenium_lib
import time

from randomwordfr import RandomWordFr

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains


def run(config, selenium_tool):
    if not config.ore_test:
        return
    # Open new tab test another case
    selenium_tool.open_tab("localhost:8069")
    time.sleep(0.5)

    # Click to Button label Crée ton clan
    selenium_tool.inject_cursor()
    selenium_tool.click_with_mouse_move(
        By.XPATH, "/html/body/div[1]/main/div/section[3]/div/div/div[2]/div/a"
    )

    # Click no account
    selenium_tool.inject_cursor()
    selenium_tool.click_with_mouse_move(
        By.XPATH, "/html/body/div[1]/main/div/form/div[3]/div[1]/a[1]"
    )

    # Trouvez les éléments du formulaire
    selenium_tool.inject_cursor()

    # Remplissez le courriel et le mot de passe
    first_name = selenium_tool.get_french_word_no_space_no_accent()
    password = first_name.lower()
    second_name = selenium_tool.get_french_word_no_space_no_accent()
    full_name = f"{first_name} {second_name}"
    domain = selenium_tool.get_french_word_no_space_no_accent().lower()

    selenium_tool.input_text_with_mouse_move(
        By.NAME, "login", f"{password}@{domain}.com"
    )
    selenium_tool.input_text_with_mouse_move(By.NAME, "name", full_name)
    selenium_tool.input_text_with_mouse_move(By.NAME, "password", password)
    selenium_tool.input_text_with_mouse_move(
        By.NAME, "confirm_password", password
    )
    selenium_tool.click_with_mouse_move(By.NAME, "accept_global_policy")
    selenium_tool.click_with_mouse_move(
        By.XPATH, "/html/body/div[1]/main/div/form/div[6]/button"
    )

    # Création du clan
    # Préparation des informations
    rw = RandomWordFr()
    dct_contain = rw.get()
    club_name = dct_contain.get("word")
    club_name_description = dct_contain.get("definition")
    dct_contain = rw.get()
    club_city_name = dct_contain.get("word")
    dct_contain = rw.get()
    institution = dct_contain.get("word")

    # Fill clan_name
    no_scroll = True
    # TODO try to use execute_script to fill text
    #  The problem occur when fill text, scroll change
    if not no_scroll:
        selenium_tool.inject_cursor()

    viewport_ele_by = By.CLASS_NAME
    viewport_ele_value = "buttons_form_container"
    selenium_tool.input_text_with_mouse_move(
        By.NAME,
        "clan_name",
        f"Club de {club_name}",
        no_scroll=no_scroll,
        viewport_ele_by=viewport_ele_by,
        viewport_ele_value=viewport_ele_value,
    )

    # Fill clan_description
    selenium_tool.input_text_with_mouse_move(
        By.XPATH,
        "/html/body/div[1]/main/div/div/section/div[2]/div[1]/textarea[1]",
        f"Définition de {club_name} : {club_name_description}",
        no_scroll=no_scroll,
        viewport_ele_by=viewport_ele_by,
        viewport_ele_value=viewport_ele_value,
    )

    # Fill clan_besoin
    selenium_tool.input_text_with_mouse_move(
        By.XPATH,
        "/html/body/div[1]/main/div/div/section/div[2]/div[1]/textarea[2]",
        f"Créer des liens sur un sujet aléatoire.",
        no_scroll=no_scroll,
        viewport_ele_by=viewport_ele_by,
        viewport_ele_value=viewport_ele_value,
    )

    # Fill clan_ville_region
    selenium_tool.input_text_with_mouse_move(
        By.NAME,
        "clan_ville_region",
        f"Ville de {club_city_name}",
        no_scroll=no_scroll,
        viewport_ele_by=viewport_ele_by,
        viewport_ele_value=viewport_ele_value,
    )

    # Fill Nom d'un organisation
    selenium_tool.input_text_with_mouse_move(
        By.NAME,
        "clan_organisation",
        f"{institution}",
        no_scroll=no_scroll,
        viewport_ele_by=viewport_ele_by,
        viewport_ele_value=viewport_ele_value,
    )

    # Fill clan_besoin
    selenium_tool.input_text_with_mouse_move(
        By.XPATH,
        "/html/body/div[1]/main/div/div/section/div[2]/div[1]/textarea[3]",
        f"Autodidacte\nPerformance\nCréation de lien humain",
        no_scroll=no_scroll,
        viewport_ele_by=viewport_ele_by,
        viewport_ele_value=viewport_ele_value,
    )

    # Créer clan
    selenium_tool.click_with_mouse_move(
        By.ID,
        "submitBtn",
        no_scroll=no_scroll,
        viewport_ele_by=viewport_ele_by,
        viewport_ele_value=viewport_ele_value,
    )

    # Force refresh angularjs
    # Move mouse on same button
    # If window didn't open, move mouse to another button
    clan_button_xpath = "/html/body/div[1]/main/div/div/div[2]/div/div/a[1]"
    hoverable = selenium_tool.driver.find_element(By.ID, "submitBtn")
    ActionChains(selenium_tool.driver).move_to_element(hoverable).perform()
    try:
        selenium_tool.get_element(By.XPATH, clan_button_xpath, timeout=5)
    except TimeoutException:
        hoverable = selenium_tool.driver.find_element(By.ID, "prevBtn")
        ActionChains(selenium_tool.driver).move_to_element(hoverable).perform()

    # Configure clan button
    selenium_tool.click_with_mouse_move(
        By.XPATH,
        clan_button_xpath,
        timeout=5,
        no_scroll=True,
    )


def fill_parser(parser):
    ore_group = parser.add_argument_group(title="ORE execution")
    ore_group.add_argument(
        "--ore_test",
        action="store_true",
        help="ore test",
    )


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""Selenium script to open web browser to ERPLibre adapted for ORE.""",
    )
    # Generate parser
    selenium_lib.fill_parser(parser)
    web_login.fill_parser(parser)
    fill_parser(parser)
    args = parser.parse_args()
    web_login.compute_args(args)
    # Instance selenium tool
    selenium_tool = selenium_lib.SeleniumLib(args)
    selenium_tool.configure()
    selenium_tool.start_record()
    # Execute
    web_login.run(args, selenium_tool)
    run(args, selenium_tool)
    selenium_tool.stop_record()
    return 0


if __name__ == "__main__":
    sys.exit(main())
