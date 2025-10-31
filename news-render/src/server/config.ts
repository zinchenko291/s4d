type Config = {
  redis: {
    username?: string,
    password?: string,
    host: string,
    port: string,
    prefix?: string
  },
  apiRoute: string
}

export default ((): Config => {
  if (import.meta.env.DEV) {
    return {
      redis: {
        username: import.meta.env.REDIS_USERNAME,
        password: import.meta.env.REDIS_PASSWORD,
        host: import.meta.env.REDIS_HOST,
        port: import.meta.env.REDIS_PORT,
        prefix: import.meta.env.REDIS_PREFIX
      },
      apiRoute: import.meta.env.API_ROUTE
    };
  }
  return {
    redis: {
      username: process.env.REDIS_USERNAME,
      password: process.env.REDIS_PASSWORD,
      host: process.env.REDIS_HOST ?? '',
      port: process.env.REDIS_PORT ?? '',
      prefix: process.env.REDIS_PREFIX
    },
    apiRoute: process.env.API_ROUTE ?? ''
  }
})();