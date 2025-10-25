# Archivo de prueba para verificar importaciones en Vercel

try:
    from tree_backend import app, application
    from tree_models import egresados_data, empleos_data
    print("✅ Importaciones exitosas")
    print(f"✅ App configurada: {app}")
    print(f"✅ Application para Vercel: {application}")
    print(f"✅ Egresados cargados: {len(egresados_data)}")
    print(f"✅ Empleos cargados: {len(empleos_data)}")
except ImportError as e:
    print(f"❌ Error de importación: {e}")
except Exception as e:
    print(f"❌ Error general: {e}")