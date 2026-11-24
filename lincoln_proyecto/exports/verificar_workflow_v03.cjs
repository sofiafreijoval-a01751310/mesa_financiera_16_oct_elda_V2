const fs = require('fs');
const path = require('path');
const assert = require('assert/strict');
const base = __dirname;
const workflow = JSON.parse(fs.readFileSync(path.join(base, 'Lincoln_Workflow_Telegram_Aprobacion_v03.json'), 'utf8'));
const node = name => workflow.nodes.find(n => n.name === name);
const execute = (name, rows, context = {}) => new Function('$input', '$', '$execution', node(name).parameters.jsCode)(
  { all: () => rows.map(json => ({ json })) },
  name => ({ first: () => ({ json: context[name] }) }),
  { id: 'UNITTEST' },
);
const person = '1000000001';
const telegram = (text, overrides = {}) => ({ update_id: 123, message: { message_id: 1, from: { id: Number(person), is_bot: false }, chat: { id: Number(person), type: 'private' }, text, ...overrides } });
const normalize = input => execute('Validar entrada Telegram', [input])[0].json;
const command = normalize(telegram('/aprobar LIN-900001-1 1'));
const proposal = { caso_id: 'LIN-900001-1', usuario: person, estado: 'PENDIENTE_APROBACION', version_propuesta: '1', decision_id: '', id: 3, vence_en: '2099-01-01T00:00:00.000Z', propuesta_json: JSON.stringify({ caso_original: { caso_id: 'LIN-900001-1', modo: 'SIMULADO' }, aprobacion_humana: false, modifica_presupuesto: false }) };
const decide = (rows, entry = command) => execute('Validar decisión humana', rows, { 'Validar entrada Telegram': entry })[0].json;
const results = [];
const test = (id, description, fn) => { try { fn(); results.push({ id, description, status: 'PASS' }); } catch (e) { results.push({ id, description, status: 'FAIL', error: e.message }); } };
test('UT01', 'Solicitud de texto autorizada se procesa', () => assert.equal(normalize(telegram('Lincoln Monterrey solicita una exhibición')).ruta, 'PROCESAR'));
test('UT02', 'Otro usuario se bloquea', () => assert.equal(normalize(telegram('hola', { from: { id: 42, is_bot: false } })).ruta, 'NO_AUTORIZADO'));
test('UT03', 'Chat grupal se bloquea', () => assert.equal(normalize(telegram('hola', { chat: { id: Number(person), type: 'group' } })).ruta, 'NO_AUTORIZADO'));
test('UT04', 'Mensaje de bot se bloquea', () => assert.equal(normalize(telegram('hola', { from: { id: Number(person), is_bot: true } })).ruta, 'NO_AUTORIZADO'));
test('UT05', 'Mensaje sin texto pide aclaración sin modelo', () => assert.equal(normalize(telegram(undefined)).ruta, 'RESPONDER'));
test('UT06', 'Más de 4000 caracteres pide corrección', () => assert.equal(normalize(telegram('x'.repeat(4001))).ruta, 'RESPONDER'));
test('UT07', 'Start devuelve instrucciones', () => assert.equal(normalize(telegram('/start')).ruta, 'RESPONDER'));
test('UT08', 'Comando correcto conserva folio y versión', () => assert.deepEqual([command.ruta, command.decision.caso_id, command.decision.version], ['DECIDIR', 'LIN-900001-1', '1']));
test('UT09', 'Comando incompleto no decide', () => assert.equal(normalize(telegram('/aprobar LIN-900001-1')).ruta, 'RESPONDER'));
test('UT10', 'Comando desconocido no llama al modelo', () => assert.equal(normalize(telegram('/transferir')).ruta, 'RESPONDER'));
test('UT11', 'Folio inexistente no se modifica', () => assert.equal(decide([{}]).aplicar, false));
test('UT12', 'Folio ambiguo no se modifica', () => assert.equal(decide([proposal, proposal]).aplicar, false));
test('UT13', 'Propietario incorrecto no puede decidir', () => assert.equal(decide([{ ...proposal, usuario: '42' }]).aplicar, false));
test('UT14', 'Versión incorrecta no puede decidir', () => assert.equal(decide([{ ...proposal, version_propuesta: '2' }]).aplicar, false));
test('UT15', 'Segunda decisión se bloquea', () => assert.equal(decide([{ ...proposal, estado: 'RECHAZADO', decision_id: 'previo' }]).aplicar, false));
test('UT16', 'Fecha inválida no permite aprobación', () => assert.equal(decide([{ ...proposal, vence_en: 'inválida' }]).aplicar, false));
test('UT17', 'Caso vencido queda VENCIDO sin aprobación humana', () => { const r = decide([{ ...proposal, vence_en: '2000-01-01T00:00:00.000Z' }]); assert.equal(r.estado, 'VENCIDO'); assert.equal(JSON.parse(r.propuesta_json).aprobacion_humana, false); });
test('UT18', 'Aprobación válida queda APROBADO_SIMULADO', () => { const r = decide([proposal]); assert.equal(r.estado, 'APROBADO_SIMULADO'); assert.equal(JSON.parse(r.propuesta_json).aprobacion_humana, true); assert.equal(JSON.parse(r.propuesta_json).modifica_presupuesto, false); });
test('UT19', 'Rechazo válido queda RECHAZADO', () => assert.equal(decide([proposal], normalize(telegram('/rechazar LIN-900001-1 1'))).estado, 'RECHAZADO'));
test('UT20', 'Entrada no autorizada falla explícitamente', () => assert.throws(() => decide([proposal], { ...command, autorizado: false })));
test('UT21', 'Modo distinto a SIMULADO falla explícitamente', () => assert.throws(() => decide([proposal], { ...command, modo: 'PRODUCCION' })));
test('UT22', 'Registro JSON corrupto falla explícitamente', () => assert.throws(() => decide([{ ...proposal, propuesta_json: '{' }])));
test('UT23', 'Folio original inconsistente falla explícitamente', () => assert.throws(() => decide([{ ...proposal, propuesta_json: JSON.stringify({ caso_original: { modo: 'SIMULADO', caso_id: 'OTRO' } }) }])));
test('UT24', 'Respaldo sin datos fijados y con fuente real restaurada', () => { assert.deepEqual(workflow.pinData || {}, {}); assert.ok(node('Validar decisión humana').parameters.jsCode.startsWith('const entrada=$("Validar entrada Telegram").first().json;')); });
test('UT25', 'Actualización requiere todas las condiciones y estado pendiente', () => { const p = node('Guardar decisión humana').parameters; assert.equal(p.matchType, 'allConditions'); assert.ok(p.filters.conditions.some(c => c.keyName === 'estado' && c.keyValue === 'PENDIENTE_APROBACION')); assert.ok(p.filters.conditions.some(c => c.keyName === 'decision_id' && c.condition === 'isEmpty')); });
const report = { generated_at: new Date().toISOString(), scope: 'Pruebas unitarias locales del JavaScript exportado; no sustituyen pruebas integrales ni la matriz oficial P01–P14.', total: results.length, passed: results.filter(r => r.status === 'PASS').length, results };
fs.writeFileSync(path.join(base, 'Resultado_Pruebas_Unitarias_v03.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
if (report.passed !== report.total) process.exitCode = 1;
