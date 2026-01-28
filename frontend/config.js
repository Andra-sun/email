/**
 * Carrega variáveis de ambiente do arquivo .env
 * Faz uma requisição para o arquivo .env e o parseia
 */

async function loadEnv() {
    try {
        const response = await fetch('./.env');
        const text = await response.text();
        const env = {};

        text.split('\n').forEach(line => {
            const trimmed = line.trim();
            if (trimmed && !trimmed.startsWith('#')) {
                const [key, ...valueParts] = trimmed.split('=');
                if (key) {
                    env[key.trim()] = valueParts.join('=').trim();
                }
            }
        });

        return env;
    } catch (error) {
        console.warn('Erro ao carregar .env:', error);
        return {};
    }
}

const envVars = await loadEnv();

export const BACKEND_URL = envVars.BACKEND_URL || 'http://localhost:8000';

export default {
    BACKEND_URL,
};
