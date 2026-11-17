import React from 'react';
import { createRoot } from 'react-dom/client';
import { Auth0Provider } from '@auth0/auth0-react';
import App from './App';
import './styles.css';

const domain = import.meta.env.VITE_AUTH0_DOMAIN as string | undefined;
const clientId = import.meta.env.VITE_AUTH0_CLIENT_ID as string | undefined;
const audience = import.meta.env.VITE_AUTH0_AUDIENCE as string | undefined;
const root = createRoot(document.getElementById('root')!);
if (domain && clientId) {
  root.render(<React.StrictMode><Auth0Provider domain={domain} clientId={clientId} authorizationParams={{ redirect_uri: window.location.origin, ...(audience ? { audience } : {}) }}><App /></Auth0Provider></React.StrictMode>);
} else {
  root.render(<React.StrictMode><App /></React.StrictMode>);
}
