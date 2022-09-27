import type { NextApiRequest, NextApiResponse } from "next";

const newLeagueStart = async (req: NextApiRequest, res: NextApiResponse) => {
  const { name, pass } = req.body as { name: string, pass: string };

  await fetch("0.0.0.0:3030/league/add", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      name: name,
      password: pass
    })
  }).then((ret) => ret.json())
    .then((ret) => {
      res.statusCode = 200;
      res.setHeader("Content-Type", "application/json");
      res.setHeader("set-cookie", [
        "cookie1=value1; SameSite=Lax",
        "cookie2=value2; SameSite=None; Secure",
      ]);
      res.setHeader("Cache-Control", "max-age=180000");
      res.end(JSON.stringify(ret));
    })
};
export default newLeagueStart;
