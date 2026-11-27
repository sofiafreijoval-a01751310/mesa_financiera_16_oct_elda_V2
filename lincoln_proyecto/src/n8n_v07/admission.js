// Ningún fallo de admisión autoriza una llamada al modelo.
const original = $('Inicializar caso').first().json;
const response = $input.first().json;
const admitted = response.statusCode === 200 && response.body?.ok === true &&
  response.body?.admitido === true && response.body?.caso_id === original.caso_id;
return [{json: {...original, control_admitido: admitted,
  control_estado: admitted ? 'ADMITIDO' : 'BLOQUEADO',
  respuesta_control: admitted ? '' : 'La evaluación no pudo admitirse. Puede tratarse de una solicitud repetida o de un control temporal. No se llamó al modelo desde esta evaluación. Consulta el folio anterior o solicita revisión del sistema.'}}];
