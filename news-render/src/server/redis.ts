import { createClient } from "redis";
import config from "./config";

export class Redis {
  redis: ReturnType<typeof createClient>;
  isReady: boolean = false;
  private readonly prefix = config.redis.prefix ?? 'news_reader';

  constructor() {
    this.redis = createClient({
      username: config.redis.username,
      password: config.redis.password,
      socket: {
        host: config.redis.host,
        port: config.redis.port
      }
    });
    this.redis.on("error", (err) => {
      console.error("[Redis] error:", err?.message ?? err);
    });

    this.connect();
  }

  async connect() {
    console.log("Start redis connection");
    await this.redis.connect();
    try {
      await this.redis.PING();
      console.log("Redis connected");
      this.isReady = true;
    } catch (e) {
      console.error(e);
    }
  }

  async getCache<T>(key: string): Promise<T | null> {
    const data = await this.redis.GET(`${this.prefix}:${key}`);
    if (data !== null) return JSON.parse(data) as T;
    return data;
  }

  async setCache<T>(key: string, value: T) {
    await this.redis.SET(`${this.prefix}:${key}`, JSON.stringify(value), { expiration: {type: 'EX', value: 15*60}, condition: 'NX' });
  }
}
