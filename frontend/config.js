/**
 * Configuração da aplicação
 * Define a URL do backend baseado no ambiente
 */

const defaults = {
    development: "http://localhost:8000",
    production: "email-production-55e8.up.railway.app",
};

const isDevelopment =
    !window.location.hostname ||
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1";

export const BACKEND_URL =
    window.BACKEND_URL ||
    (isDevelopment ? defaults.development : defaults.production);

export default {
    BACKEND_URL,
};
