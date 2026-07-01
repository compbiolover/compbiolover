# Self-hosting the GitHub stats cards

The profile README renders two cards from
[`github-readme-stats`](https://github.com/anurag-hazra/github-readme-stats):

- **GitHub stats** — includes the circular **grade / rank badge** (S, A+, A, B…)
- **Top languages** — the "Most Used Languages" bar

The README points these at a **self-hosted** instance rather than the shared
public one (`github-readme-stats.vercel.app`). The public instance is heavily
rate-limited: the main stats endpoint (`/api`) makes many GitHub API calls and
is the first to fail, which is why the grade card intermittently disappears
while the top-languages card keeps working. Your own instance has its own rate
limit and stays reliable.

## One-time deploy (~10 minutes)

You need a GitHub account and a Vercel account (the free Hobby tier is enough).

### 1. Create a GitHub personal access token (PAT)

1. Go to <https://github.com/settings/tokens> → **Generate new token** →
   **classic**.
2. Name it e.g. `github-readme-stats`.
3. No scopes are required for **public** repos only. If you also want private
   repos counted, check the **`repo`** scope.
4. Generate it and copy the token (you won't see it again).

### 2. Deploy github-readme-stats to Vercel

1. Fork <https://github.com/anurag-hazra/github-readme-stats> to your account
   (or use "Deploy" from that repo's README).
2. Go to <https://vercel.com/new>, **Import** your fork.
3. **Project name:** set it to exactly

   ```
   github-readme-stats-compbiolover
   ```

   This matters — it makes the production URL
   `https://github-readme-stats-compbiolover.vercel.app`, which is the domain
   already baked into `README.md`. If you use a different name, update the two
   `img` `src` URLs in `README.md` to match.
4. Under **Environment Variables**, add:

   | Name         | Value                        |
   | ------------ | ---------------------------- |
   | `PAT_1`      | the token from step 1        |

   (You can add `PAT_2`, `PAT_3`, … with additional tokens later to raise the
   effective rate limit, but one is plenty for a personal profile.)
5. Click **Deploy** and wait for the build to finish.

### 3. Verify

Open these in a browser — both should render an SVG (the first one shows the
grade/rank circle):

- <https://github-readme-stats-compbiolover.vercel.app/api?username=compbiolover&show_icons=true&hide_border=true&theme=default>
- <https://github-readme-stats-compbiolover.vercel.app/api/top-langs/?username=compbiolover&layout=compact&hide_border=true&theme=default>

Then reload your profile at <https://github.com/compbiolover>. The grade should
now show consistently.

## Notes

- The grade badge always renders on the main stats card unless you add
  `&hide_rank=true`. There's nothing to enable — it was only missing because
  the whole card image was failing to load.
- You can style the rank with `&rank_icon=percentile` or `&rank_icon=github`,
  and change `&theme=` to any
  [supported theme](https://github.com/anurag-hazra/github-readme-stats#themes).
- Keep your fork updated periodically so the instance stays current with
  upstream fixes.
