"""Loop de recuperación con reloj, intentos y reserva de costo antes de cada intento."""
import time

def recuperar(consulta,guardian,case_id,user_id,request_id,trace,*,allowed_user,max_attempts=3,seconds=10,bound_usd='0.01'):
    if isinstance(max_attempts,bool) or not isinstance(max_attempts,int) or not 1<=max_attempts<=3:
        raise ValueError('Máximo tres intentos')
    if not 0<seconds<=10: raise ValueError('Máximo diez segundos')
    start=time.monotonic()
    for attempt in range(1,max_attempts+1):
        if time.monotonic()-start>=seconds: return {'estado':'TIMEOUT'}
        admission=guardian.admit(f'{request_id}:{attempt}',case_id,user_id,allowed_user,bound_usd)
        if not admission['admitido']:
            trace.append({'loop':'recuperacion','intento':attempt,**admission})
            return {'estado':admission['motivo']}
        try:
            result=consulta()
            # callback local; una integración HTTP DEBE pasar timeout restante al transporte.
            if time.monotonic()-start>=seconds: return {'estado':'TIMEOUT'}
            if not isinstance(result,dict) or result.get('caso_id')!=case_id:
                trace.append({'loop':'recuperacion','intento':attempt,'estado':'ESQUEMA_INVALIDO'})
                return {'estado':'ESCALAR'}
            trace.append({'loop':'recuperacion','intento':attempt,'estado':'OK','cota_usd':bound_usd})
            return {'estado':'OK','datos':result}
        except (TimeoutError,ConnectionError):
            trace.append({'loop':'recuperacion','intento':attempt,'estado':'ERROR_TRANSITORIO','cota_usd':bound_usd})
    return {'estado':'ESCALAR'}
