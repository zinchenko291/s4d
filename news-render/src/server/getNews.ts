import axios from "axios";
import { Redis } from "./redis";
import config from "./config";

const instance = axios.create({
  baseURL: config.apiRoute,
});

let redis: Redis;

try {
  redis = new Redis();
} catch (e) {
  console.error(e);
  console.error("Working without cache");
}

export type NewsDto = {
  id: string;
  summary: string;
}

async function fetchNews(newsId: string): Promise<NewsDto> {
  console.log("[fetchNews]: Start fetch news");
  const response = await instance.get(`/${newsId}`);
  console.log("[fetchNews]: News fetched");
  return response.data;
}

export async function getNews(newsId: string): Promise<NewsDto> {
  console.log("[getNews]: Start fetching news " + newsId);
  try {
    if (redis.redis && redis.redis.isOpen && redis.isReady) {
      console.log("[getNews]: Fetch cache");
      const data = await redis.getCache<NewsDto>(newsId);
      console.log("[getNews]: Cache fetched");
      if (data !== null) return data;
  
      console.log("[getNews]: Cache missed");

      const fetch = await fetchNews(newsId);
      console.log("[getNews]: Save cache");
      new Promise(() => redis.setCache(newsId, fetch)).catch(console.error);
      return fetch;
    }
  } catch (e: any) {
    console.error(`[getNews]: Error ${e?.status}`);
    throw e;
  }
  
  console.log("[getNews]: Fetch without Redis");
  return await fetchNews(newsId);
}