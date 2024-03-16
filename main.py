from app import funciones
import os


def main():
    while True:     
        os.system('cls')           
        print("\tBienvenido a la aplicación de música.".upper())
        print( "***Menú principal***".upper())       
        
        print("1. Registrar nuevo usuario")
        print("2. Iniciar sesión")
        print("3. Restaurar datos por defecto")
        print("4. Estadisticas")
        print("5. Salir")
        opc = funciones.validate_integer_input_min_max("Seleccione una opción: ", 1, 5)
        if opc == 1:
            user = funciones.create_new_user()
            print(f"Usuario creado: {user} exitosamente.")   
        elif opc == 2:
            funciones.login_user()
        elif opc == 3:
            confirm = input("Está a punto de restaurar los datos por defecto. Esto borrará todos los datos actuales. ¿Está seguro? (s/n): ")
            if confirm.lower() == 's':
                codes = funciones.restore_default_data()
                print("Datos restaurados:")
                print(f"Usuarios: code response {codes['users']}")
                print(f"Álbumes y Canciones: code response {codes['albums']}")
                print(f"Playlists: code response {codes['playlists']}")
            else:
                print("Operación cancelada.")
         
        elif opc == 4:
            funciones.show_statistics()
        elif opc == 5:
            print("Saliendo de la aplicación...")
            break
        
        else:
            print("Opción inválida.")
        

        


if __name__ == "__main__":
    main()
