# Formation-TODO
A list of action items to form the Bitgrid SIG.

- [ ] **1. Charter & Governance**
    - [ ] Draft Charter - a couple of pages outlining the mission, deliverables, defining what's in-scope/out-of-scope
    - [ ] Define Officer Roles
        - Chair
            - Interim (founder) (Pre-Ratification)
            - Post-Ratification
        - Secretary
        - WG Leads
        - Etc
    - [ ] Specify term limits & ratification process (e.g. vote after 6 months or 50 members)
    - [ ] **Decision Model:** Lazy consensus with NACK-driven objections
        - Proposals announced via GitHub Issues/PRs
        - **Review Window:** 14 calendar days for objections (silence = consent)
        - **NACK Period:** Objectors must file `NACK: <reason>` within 14 days
        - **Resolution Window:** Authors/WG leads address objections within 7 calendar days
        - **Escalation:** Unresolved objections escalate to SIG Chair or arbitration committee
- [ ] **2. Working Groups**
    - [ ] **Grid Protocol WG:** extension of `HTTP`/`HTTPS` and `grid://` URI syntax & semantics
    - [ ] **DNS & TLD WG:** custom DNS stack, community TLD governance
    - [ ] **Markup & Styling WG:** grid-markup language & style spec
    - [ ] **Runtime WG:** Lua sandbox API, WASM inclusion, low-power runtime requirements
    - [ ] **Conformance WG:** test suite, validator CLI, certification process
- [ ] **3. Membership & Onboarding**
    - [ ] **Define tiers:** Contributor, Committer, Maintainer, etc
    - [ ] Publish Code of Conduct + onboarding guide
    - [ ] Open calls for WG membership
- [ ] **4. Infrastructure & Tools**
    - [ ] Create GitHub org & repos for charter, specs, test suite
        - [X] Org
        - [ ] Repos
            - [ ] Charter
            - [ ] Specs
            - [ ] Test Suite
    - [ ] Set up mailing list, Discord/Matrix channels
    - [ ] Issue RFC template; schedule bi-weekly WG meetings
- [ ] **5. Spec Drafting**
    - [ ] **Kick Off:** Start with the grid protocol, including the `grid://` URI spec (Protocol WG)
    - [ ] **Parallel Drafts:** DNS extensions, markup/styling, Lua API
    - [ ] Conformance WG builds test harness alongside spec work
- [ ] **6. Public Presence & Outreach**
    - [ ] **Main Website:** Charter, WG portal, calendar, meeting archives
    - [ ] **Main Gridsite:** Charter, WG portal, calendar, meeting archives
    - [ ] **WG Microsites:** lightweight docs for each WG's specs and roadmap
    - [ ] **Demonstration Gridsites:** host example gridsites (e.g. `grid://demo.bitgrid.sig/index.ext`)
    - [ ] **Extra-Community Outreach:** Announce to communities such as: Fantasy Consoles, Raspberry Pi,
          General Lua Communities, Embedded Communities such as NodeMCU, Sipeed products, etc
    - [ ] **Hold Inaugural Plenary:** review charter, confirm Interim Chair, recruit WG leads
- [ ] **7. Milestones & Maintenance**
    - [ ] v0.1 Protocol & DNS spec in 60 days
    - [ ] First conformance tests released 30 days after spec
    - [ ] Ratification vote for permanent Chair inn accordance with The Charter
    - [ ] Quarterly spec reviews; annual certification renewal
    - [ ] Maintain public registry of participating communities


