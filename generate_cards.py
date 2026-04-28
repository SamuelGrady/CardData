OUTPUT_DIR = "cards"
TEMPLATE_CARDS = ["template_c.svg", "template_d.svg", "template_h.svg", "template_s.svg"]
VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

def generate_card(template, value, save_name):
    with open(template, "r") as file:
        card_data = file.read()
    with open(f"{OUTPUT_DIR}/{save_name}", "w") as file:
        file.write(card_data.replace("?a", value))

for template in TEMPLATE_CARDS:
    for value in VALUES:
        save_name = template.replace("template_", value)
        generate_card(template, value, save_name)