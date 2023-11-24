import datetime
from kivymd.app import MDApp
from kivy.app import App
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import OneLineAvatarIconListItem, MDList
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import SlideTransition
from database_manager import *

class MyAppWindow(MDBoxLayout):
    pass

class TelaLogin(MDScreen):
    pass
        
class TelaServicos(MDScreen):
    pass
        
class TelaCadastro(MDScreen):
    pass
        
class TelaReclamacao(MDScreen):
    pass
        
class TelaConsulta(MDScreen):
    pass
        
class TelaRecuperarSenha(MDScreen):
    pass
        
class ItemConfirm(OneLineAvatarIconListItem, ButtonBehavior):
    def __init__(self, **kwargs):
        super(ItemConfirm, self).__init__(**kwargs)
        self.checkbox = MDCheckbox()
        self.checkbox.bind(active=self.on_checkbox_active)
        self.bind(on_release=self.on_item_click)

    def on_checkbox_active(self, instance_checkbox, value):
        if value:
            print(f"Checkbox {self.text} is active.")
        else:
            print(f"Checkbox {self.text} is inactive.")

    def on_item_click(self, *args):
        # Adiciona o item à lista
        app = MDApp.get_running_app()
        app.add_selected_option(self.text)
        
class ItemConfig(OneLineAvatarIconListItem, ButtonBehavior):
    def __init__(self, **kwargs):
        super(ItemConfig, self).__init__(**kwargs)

    def on_item_click(self, *args):
        # Adiciona o item à lista
        app = MDApp.get_running_app()
        app.add_selected_option(self.text)
        self.close_conf()
        
class main(MDApp):    
    
    def build(self):        
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        self.dialog = None
        self.dialog_option = None
        self.conf = None
        self.selected_options = []  # Lista para armazenar opções selecionadas
        
        self.my_app_window = MyAppWindow()    
        return self.my_app_window
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_screen_switch_state = True 
    
    def show_confirmation_dialog(self, text, *args):
        self.dialog = None
        if not self.dialog:
            text = text
            label = MDLabel(text=text, halign="center", theme_text_color="Secondary")
            buttons = [
                MDRaisedButton(
                    text="Ok",
                    pos_hint={"center_x": 0.5},
                    on_release=self.close_dialog,
                ),
            ]
            self.dialog = MDDialog(
                title="",
                type="custom",
                content_cls=label,
                buttons=buttons,
                size_hint=(None, None),
                height=dp(200),
                width=dp(400),
            )        
        self.dialog.open()

    def show_options_dialog(self, *args):
        if not self.dialog_option:
            items = [
                ItemConfirm(text="Buraco"),
                ItemConfirm(text="Iluminação"),
                ItemConfirm(text="Entulho"),
            ]
            buttons = [
                MDRaisedButton(
                    text="CANCEL",
                    pos_hint={"center_x": 0.2, "center_y": 0.1},
                    on_release=self.close_dialog_option,
                ),
            ]
            self.dialog_option = MDDialog(
                title="Escolha uma Opção",
                type="confirmation",
                items=items,
                buttons=buttons,
                size_hint=(None, None),
                height=dp(200),
                width=dp(300),
            )
        self.dialog_option.open()

    def close_dialog(self, *args):
            self.dialog.dismiss()
    
    def close_dialog_option(self, *args):
            self.dialog_option.dismiss()

    def add_selected_option(self, option):
        self.root.ids.problema_input.text = option
        self.selected_options = [option]

        # Use os valores como desejar (por exemplo, salvá-los em um banco de dados)
        
        selected_item_label = self.my_app_window.ids.selected_item_label
        selected_item_label.text = ""
        
        # Fecha a caixa de diálogo
        self.close_dialog_option()
        
    def cadastrar_municipe(self, text):
        # Chame a função save_to_database do arquivo database_manager.py
        
        nome = self.root.ids.nome_input.text
        email = self.root.ids.email_input.text
        senha = self.root.ids.senha_input.text
        senha2 = self.root.ids.senha2_input.text
        
        if len(email) < 6 or len(senha) < 6:
            self.show_confirmation_dialog("Email e senha 6 digitos no minimo")
        elif senha != senha2:
            self.show_confirmation_dialog("Confirmação de senha diferente da senha")
        elif len(nome) < 3:
            self.show_confirmation_dialog("Nome 3 digitos no minimo")
        else:
            self.text = text
            validate = True
            save_municipe(nome, email, senha, validate)

            # Mostre a mensagem
            self.show_confirmation_dialog(self.text)
    
    def login(self):
        screen_manager = self.root.ids.screen_manager
        email = self.root.ids.email_login.text
        senha = self.root.ids.senha_login.text
        
        if len(email) < 6 or len(senha) < 6:
            pass
        else:
            if validar_login(email, senha):
                screen_manager.current = "tela_servicos"
            else:
                self.show_confirmation_dialog("Email ou Senha inválido")
    
    def cadastrar_reclamacao(self, text):
        # Chame a função save_to_database do arquivo database_manager.py
        option = self.root.ids.problema_input.text
        problema = option
        bairro = self.root.ids.bairro_input.text
        rua = self.root.ids.rua_input.text
        descricao = self.root.ids.descricao_input.text
        email = self.root.ids.email_login.text
        senha = self.root.ids.senha_login.text
    
        login_result = validar_login(email, senha)
        if login_result is not None:
            idMunicipe, nomeMunicipe = login_result
        validate = True
        if save_reclamacao(idMunicipe, nomeMunicipe, problema, bairro, rua, descricao, validate):
            self.show_confirmation_dialog(text)
    
    def exibir_consulta(self, *args):
        email = self.root.ids.email_login.text
        senha = self.root.ids.senha_login.text
        login_result = validar_login(email, senha)

        if login_result is not None:
            idMunicipe, nomeMunicipe = login_result
            reclamacoes = get_reclamacoes(idMunicipe)

            if reclamacoes:
                print(reclamacoes[0][2])
                # Ajuste aqui para acessar corretamente os elementos da lista
                self.root.ids.protocolo_label.text = f'{reclamacoes[0][2]}'
                self.root.ids.requerente_label.text = f'{reclamacoes[0][3]}'
                self.root.ids.problema_label.text = f'{reclamacoes[0][4]}'
                self.root.ids.bairro_label.text = f'{reclamacoes[0][5]}'
                self.root.ids.status_label.text = f'{reclamacoes[0][8]}'
            else:
                self.show_confirmation_dialog('Você não tem reclamações ativas')
        else:
            self.show_confirmation_dialog('Login inválido')
    
    def navigate_to_login(self):
        screen_manager = self.root.ids.screen_manager
        screen_manager.transition = SlideTransition(direction="left")
        self.root.ids.screen_manager.current = "tela_login"
    
    def navigate_to_cadastro(self):
        screen_manager = self.root.ids.screen_manager
        screen_manager.transition = SlideTransition(direction="left")
        self.root.ids.screen_manager.current = "tela_cadastro"
    
    def navigate_to_home(self):
        screen_manager = self.root.ids.screen_manager
        screen_manager.transition = SlideTransition(direction="right")
        self.root.ids.screen_manager.current = "home"
    
    def seta_voltar(self):
        screen_manager = self.root.ids.screen_manager
        current_screen = screen_manager.current

        # Defina as transições conforme necessário
        screen_manager.transition = SlideTransition(direction="right")
        
        if current_screen == "tela_login":
            screen_manager.current = "home"
        elif current_screen in ["tela_servicos", "tela_cadastro", "tela_recuperar_senha"]:
            screen_manager.current = "tela_login"
        elif current_screen in ["tela_consulta", "tela_reclamacao"]:
            screen_manager.current = "tela_servicos"
    
    def switch_theme_style(self):
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )
    
    def configuracoes(self, *args):
        if not self.conf:
            items = [
                ItemConfig(text="Historico"),
                ItemConfig(text="Politica de Privacidades"),
                ItemConfig(text="Enviar feedback"),
                ItemConfig(text="Ajuda"),
            ]            
            self.conf = MDDialog(
                type="confirmation",
                items=items,
                pos_hint={'right': .98, 'top': .98},
                size_hint=(None, None),
                height=dp(200),
                width=dp(300),
            )
        self.conf.open()
        
    def close_conf(self, *args):
        print("Clicou")
        self.conf.dismiss()

if __name__ == '__main__':
    main().run()
