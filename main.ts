import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const envDir = process.env.MAKEFUN_OUTPUT_DIR;
const targetDir = path.resolve(envDir && envDir.length > 0 ? envDir : "output");

const sourceFile = path.join(here, "POST.json");
const copiedFile = path.join(targetDir, "POST.json");

mkdirSync(targetDir, { recursive: true });
copyFileSync(sourceFile, copiedFile);

const originalBytes = readFileSync(sourceFile);
const copiedBytes = readFileSync(copiedFile);

if (!originalBytes.equals(copiedBytes)) {
  console.error(`Error: byte mismatch after copying POST.json to ${copiedFile}`);
  process.exit(1);
}

console.log(`Verified POST.json copied to ${copiedFile} (${copiedBytes.byteLength} bytes).`);
