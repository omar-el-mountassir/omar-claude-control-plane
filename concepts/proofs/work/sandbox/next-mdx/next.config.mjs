import createMDX from "@next/mdx";
const withMDX = createMDX();
export default withMDX({
  pageExtensions: ["mdx","tsx","ts","js"],
  experimental: { externalDir: true } // allow imports from ../../../components and ../../../current/data
});