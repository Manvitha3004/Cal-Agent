import { io } from "socket.io-client";

export const socket = io("/ws", {
  autoConnect: false,
  transports: ["websocket"]
});
