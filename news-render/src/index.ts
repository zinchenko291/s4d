import express from 'express';
import { handler as ssrHandler } from '../dist/server/entry.mjs';
import { initRedisClient } from './server/redis';

async function main() {
  const app = express();

  app.use('/', express.static('dist/client/'));
  app.use(ssrHandler);

  app.listen(8080);
}

void main();
