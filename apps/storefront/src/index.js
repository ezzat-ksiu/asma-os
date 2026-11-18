export default {
  async fetch(request, env) {
    const response = await env.ASSETS.fetch(request);
    if (response.status === 404) {
      const url = new URL(request.url);
      return await env.ASSETS.fetch(new URL('/index.html', url.origin));
    }
    return response;
  }
};
