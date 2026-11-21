"""MindFrame interactive IT lab. Run: python -m streamlit run app.py"""
import streamlit as st
from evaluator import evaluate

st.set_page_config(page_title="MindFrame | IT Lab", page_icon="🧠", layout="wide")
st.markdown('''<style>
.stApp{background:#102B30;color:#ECF8F6}.block-container{max-width:1100px;padding-top:1.4rem}
h1,h2,h3{color:#ECF8F6!important}p,li,label{color:#D9E9E7!important}
div.stButton>button[kind="primary"]{background:#FF9A5C;color:#102B30;border:0;font-weight:700}
div.stButton>button{border-color:#4A7777}
[data-testid="stMetric"]{background:#20464B;padding:12px;border-radius:12px}
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea{background:#17373C;color:#ECF8F6}
</style>''', unsafe_allow_html=True)

DEFAULT = dict(stage=0, candidate_name='', history=[], logs=[], connected=False, saved_profile=True,
               adapter_enabled=True, credentials_updated=False, outage=False,
               notes="", resolution="", follow_answer="", report=None, commands=0)
for k,v in DEFAULT.items():
    if k not in st.session_state:
        st.session_state[k] = v.copy() if isinstance(v,list) else v
s=st.session_state
if 'candidate_reports' not in s:
    s.candidate_reports = []
if 'selected_report_id' not in s:
    s.selected_report_id = None
if 'demo_role' not in s:
    s.demo_role = None
if 'demo_organization' not in s:
    s.demo_organization = 'Campus IT Department'

def record(action, result):
    s.history.append(action)
    s.logs.append(result)
    return result

def terminal(command):
    c=' '.join(command.strip().lower().split())
    if not c: return 'Type a command. Use help to see supported commands.'
    s.commands += 1
    if c in ('help','?'):
        out=('Available simulated commands:\n'
             '  ipconfig /all\n  ping 8.8.8.8\n  netsh wlan show interfaces\n'
             '  netsh wlan show profiles\n  netsh wlan show profile name=OfficeNet\n'
             '  netsh wlan delete profile name=OfficeNet\n  netsh wlan connect name=OfficeNet\n'
             '  netsh interface set interface name="Wi-Fi" admin=enabled\n'
             '  netsh interface set interface name="Wi-Fi" admin=disabled\n'
             'These commands affect only the fictional lab.')
    elif c=='ipconfig /all':
        out='Wireless LAN adapter Wi-Fi\n  Adapter: '+('Enabled' if s.adapter_enabled else 'Disabled')+'\n  IPv4: '+('192.168.10.42' if s.connected else 'Not assigned')+'\n  Gateway: '+('192.168.10.1' if s.connected else 'Not available')
    elif c=='ping 8.8.8.8':
        out='Reply from 8.8.8.8: bytes=32 time=18ms' if s.connected else 'Request timed out. No network connection.'
    elif c=='netsh wlan show interfaces':
        out='Interface: Wi-Fi\nState: '+('connected' if s.connected else 'disconnected')+'\nSSID: '+('OfficeNet' if s.connected else 'None')+'\nSignal: 94%'
    elif c=='netsh wlan show profiles':
        out='Saved profiles: '+('OfficeNet' if s.saved_profile else '(none)')
    elif c=='netsh wlan show profile name=officenet':
        out='Profile: OfficeNet\nSecurity: WPA2-Enterprise\nLast authentication: '+('Success' if s.connected else 'Failed (outdated saved credentials)') if s.saved_profile else 'Profile OfficeNet not found.'
    elif c=='netsh wlan delete profile name=officenet':
        s.saved_profile=False;s.connected=False
        out='Profile OfficeNet removed. Reconnect through Wi-Fi Settings with updated credentials.'
    elif c=='netsh wlan connect name=officenet':
        if not s.adapter_enabled: out='Cannot connect: Wi-Fi adapter disabled.'
        elif not s.saved_profile: out='Profile not found. Use Wi-Fi Settings to reconnect.'
        elif not s.credentials_updated: out='Connection failed: authentication error. Saved credentials are outdated.'
        else: s.connected=True;out='Connection request completed successfully. Verify with ping.'
    elif c in ('netsh interface set interface name="wi-fi" admin=enabled','netsh interface set interface name=wi-fi admin=enabled'):
        s.adapter_enabled=True;out='Wi-Fi adapter enabled.'
    elif c in ('netsh interface set interface name="wi-fi" admin=disabled','netsh interface set interface name=wi-fi admin=disabled'):
        s.adapter_enabled=False;s.connected=False;out='Wi-Fi adapter disabled.'
    else: out='Command not recognized in this simulated lab. Type help for supported commands.'
    return record('Terminal: '+command, out)

def gui(action):
    if action=='Inspect network status':
        out='Wi-Fi '+('enabled' if s.adapter_enabled else 'disabled')+'. OfficeNet visible. '+('Connected.' if s.connected else 'Authentication failed.')
    elif action=='Check coworker connectivity':
        out='Three coworkers are connected to OfficeNet. The issue appears specific to Alex’s laptop.'
    elif action=='Inspect saved Wi-Fi profile':
        out='OfficeNet profile: '+('Saved; last authentication failed.' if s.saved_profile else 'Not saved.')
    elif action=='Forget OfficeNet':
        s.saved_profile=False;s.connected=False;out='OfficeNet forgotten. Reconnect using updated credentials.'
    elif action=='Reconnect with updated credentials':
        if not s.adapter_enabled: out='Cannot reconnect: Wi-Fi adapter is disabled.'
        else:
            s.credentials_updated=True;s.saved_profile=True;s.connected=True
            out='Updated credentials accepted. Connected to OfficeNet. Verify with ping.'
    elif action=='Reset Wi-Fi adapter':
        s.adapter_enabled=True;s.connected=False;out='Adapter reset. Authentication error remains until credentials are updated.'
    elif action=='Restart shared office router':
        s.outage=True;s.connected=False;out='Shared router restarted. Three coworkers temporarily lost access; Alex still cannot connect.'
    else: out='No action taken.'
    return record('Desktop: '+action,out)

def lab_observations():
    """Evidence derived from this version of the simulated lab, not old action names."""
    actions = s.history
    observations = []
    checks = [a for a in actions if a.startswith('Desktop: Inspect') or
              a == 'Desktop: Check coworker connectivity' or
              any(a.lower().startswith('terminal: ' + x) for x in
                  ('ipconfig', 'ping', 'netsh wlan show'))]
    if checks:
        observations.append(f"Performed {len(checks)} network diagnostic check(s).")
    if any(a == 'Desktop: Reconnect with updated credentials' for a in actions):
        observations.append('Attempted to reconnect using updated Wi-Fi credentials.')
    if any(a.lower().startswith('terminal: ping 8.8.8.8') for a in actions):
        observations.append('Used a ping test to check connectivity.')
    if s.connected:
        observations.append('OfficeNet was connected at the end of the simulation.')
    else:
        observations.append('OfficeNet was not connected at the end of the simulation.')
    if s.outage:
        observations.append('Restarted the shared router, interrupting coworkers.')
    failed = sum('Command not recognized' in output for output in s.logs)
    if failed:
        observations.append(f'{failed} unsupported command attempt(s) recorded.')
    return observations

def reset_lab(candidate_name):
    """Start a fresh simulation without modifying any previously saved reports."""
    for k, v in DEFAULT.items():
        s[k] = v.copy() if isinstance(v, list) else v
    s.candidate_name = candidate_name
    s.demo_role = 'student'
    s.stage = 0

def save_completed_report():
    """Save an independent snapshot; later sign-ins cannot rename old evidence."""
    import copy
    snapshot = {
        'id': len(s.candidate_reports) + 1,
        'candidate_name': s.candidate_name,
        'history': list(s.history), 'logs': list(s.logs),
        'connected': s.connected, 'outage': s.outage,
        'notes': s.notes, 'resolution': s.resolution,
        'follow_answer': s.follow_answer,
        'report': copy.deepcopy(s.report),
    }
    s.candidate_reports.append(snapshot)
    s.selected_report_id = snapshot['id']

# Mock sign-in: this is a presentation prototype, NOT authentication.
if s.demo_role is None:
    st.markdown('## 🧠 MindFrame')
    st.caption('MORE THAN MEETS THE RÉSUMÉ.')
    st.title('Welcome to MindFrame')
    st.write('Explore job-related technical skills from either side of the experience.')
    st.info('DEMO MODE — No accounts are created, identities are not verified, and no real access controls are provided. Use fictional information only.')
    selected = st.radio('Choose a demo experience', ['Student / Candidate', 'Employer / Reviewer'], horizontal=True)
    with st.form('mock_sign_in'):
        if selected == 'Student / Candidate':
            display_name = st.text_input('Candidate name', value=s.candidate_name or 'Jamie Jones', max_chars=80)
            st.caption('Your name will appear on your skills report.')
        else:
            display_name = st.text_input('Demo organization', value=s.demo_organization, max_chars=80)
            st.caption('The employer preview only shows evidence generated in this demo session.')
        enter = st.form_submit_button('Enter demo →', type='primary')
    if enter:
        if not display_name.strip():
            st.error('Please enter a name to continue.')
        else:
            if selected == 'Student / Candidate':
                reset_lab(display_name.strip())
            else:
                s.demo_organization = display_name.strip()
                s.demo_role = 'employer'
            st.rerun()
    st.stop()

# Keep navigation in the main content area so it is not clipped by the toolbar.
if st.button('← Switch demo role', key='switch_role'):
    s.demo_role = None
    st.rerun()

if s.demo_role == 'employer':
    st.markdown('## 🧠 MindFrame')
    st.caption('MORE THAN MEETS THE RÉSUMÉ. · Employer demo')
    st.subheader('Employer review portal')
    st.write('**Organization:**', s.demo_organization)
    st.caption('Fictional reports from this browser session only. No real authentication or private data storage.')
    reports = s.candidate_reports
    if not reports:
        st.info('No candidate reports yet. Switch demo role, complete a student lab, and return here to view the report.')
        st.stop()
    c1,c2=st.columns(2)
    c1.metric('Completed candidate labs',len(reports))
    c2.metric('Distinct demo candidates',len(set(r['candidate_name'] for r in reports)))
    st.markdown('### Candidate reports')
    for r in reversed(reports):
        a,b,c=st.columns([3,2,1])
        a.write('**'+r['candidate_name']+'**')
        b.write('Connected' if r['connected'] else 'Not resolved')
        if c.button('View report',key='view_report_'+str(r['id'])):
            s.selected_report_id = r['id']
            st.rerun()
    selected = next((r for r in reports if r['id']==s.selected_report_id),None)
    if selected is None:
        st.info('Choose View report to inspect the candidate’s work.')
        st.stop()
    st.divider()
    st.subheader('Evidence report: '+selected['candidate_name'])
    active = selected
else:
    active = None

if s.demo_role == 'employer':
    s.stage = 3
else:
    st.markdown('## 🧠 MindFrame')
    st.caption('MORE THAN MEETS THE RÉSUMÉ.  ·  Fictional skills demonstration')
if s.demo_role == 'student':
    steps=['Briefing','Workstation','Resolution','Your report']
    cols=st.columns(4)
    for i,(col,name) in enumerate(zip(cols,steps)):
        col.markdown(('🟢 ' if i==s.stage else '○ ')+f'**{i+1}. {name}**')
    st.progress((s.stage+1)/4)

if s.stage==0:
    st.subheader('Support ticket IT-1042')
    st.info('**Alex Morgan (fictional):** My laptop won’t connect to OfficeNet Wi-Fi, and I have a meeting soon. Can you help?')
    st.write('You are the IT support technician. Explore a simulated workstation, diagnose the problem, attempt a repair, and verify the result. Your actions are recorded for evidence-based review.')
    st.warning('This is a safe simulation. No commands run on your actual computer or network.')
    st.write('**Signed in as (demo):**', s.candidate_name)
    if st.button('Start lab →', type='primary'):
        s.stage = 1
        st.rerun()

elif s.stage==1:
    st.subheader('Alex’s remote workstation')
    a,b,c=st.columns(3)
    a.metric('Network', 'Connected' if s.connected else 'Disconnected')
    b.metric('Wi-Fi adapter','Enabled' if s.adapter_enabled else 'Disabled')
    c.metric('Recorded actions',len(s.history))
    terminal_tab,settings_tab,notes_tab=st.tabs(['⌨️ Command Prompt','🖥️ Wi-Fi Settings','📝 Activity log'])
    with terminal_tab:
        st.code('Microsoft Windows [Simulated]\nC:\\Users\\Alex> '+('OfficeNet connected' if s.connected else 'OfficeNet disconnected'),language='text')
        with st.form('terminal_form',clear_on_submit=True):
            cmd=st.text_input('Enter a command (type help to see supported commands)',placeholder='ipconfig /all')
            run=st.form_submit_button('Run command',type='primary')
        if run: terminal(cmd)
        if s.logs: st.code(s.logs[-1],language='text')
    with settings_tab:
        st.write('**Wi-Fi:** '+('On' if s.adapter_enabled else 'Off'))
        st.write('**OfficeNet:** '+('Connected' if s.connected else 'Not connected'))
        st.caption('Choose actions as you would in a remote desktop. These change the lab state.')
        options=['Inspect network status','Check coworker connectivity','Inspect saved Wi-Fi profile',
                 'Forget OfficeNet','Reconnect with updated credentials','Reset Wi-Fi adapter','Restart shared office router']
        for start in range(0,len(options),2):
            cs=st.columns(2)
            for col,opt in zip(cs,options[start:start+2]):
                if col.button(opt,key='gui_'+opt,use_container_width=True): gui(opt);st.rerun()
    with notes_tab:
        if not s.history: st.caption('Your activity will appear here as you work.')
        for i,(act,out) in enumerate(zip(s.history,s.logs),1):
            with st.expander(f'{i}. {act}',expanded=i==len(s.history)): st.code(out,language='text')
    st.divider()
    if s.connected: st.success('OfficeNet is connected. Verify the fix using ping 8.8.8.8 before finishing.')
    if s.outage: st.warning('A shared router restart interrupted coworkers. Consider this in your resolution notes.')
    if st.button('Continue to resolution notes →',type='primary',disabled=not s.history): s.stage=2;st.rerun()

elif s.stage==2:
    st.subheader('Document your troubleshooting')
    st.write('Brief notes are fine. Explain what the evidence showed and why you chose your actions.')
    with st.form('notes_form'):
        notes=st.text_area('What did you discover? Why did you choose those steps?',value=s.notes,height=110)
        resolution=st.text_area('What did you change, and how did you verify the outcome?',value=s.resolution,height=110)
        st.info('New information: Alex mentions changing their OfficeNet password yesterday. How does this affect your diagnosis?')
        follow=st.text_area('How would you respond to this new information?',value=s.follow_answer,height=100)
        submit=st.form_submit_button('Generate evidence-based report',type='primary')
    if submit:
        if not all(x.strip() for x in (notes,resolution,follow)):
            st.error('Please complete the three brief notes before continuing.')
        else:
            s.notes,s.resolution,s.follow_answer=notes,resolution,follow
            try: key=st.secrets.get('GEMINI_API_KEY','')
            except Exception: key=''
            with st.spinner('Reviewing recorded evidence with Gemini...'):
                s.report=evaluate(s.history,notes,resolution,follow,key)
                # The earlier evaluator checks obsolete action labels; use actual lab evidence.
                s.report['observations'] = lab_observations()
            save_completed_report()
            s.stage=3;st.rerun()
    if st.button('← Back to workstation'): s.stage=1;st.rerun()

else:
    st.subheader('Employer review dashboard' if s.demo_role == 'employer' else 'Your skills report')
    st.caption('AI-assisted evidence review · Human verification required · Mock sign-in only')
    if s.demo_role == 'employer':
        st.write('**Reviewer organization:**', s.demo_organization)
    st.write('**Candidate:**', active['candidate_name'] if active else s.candidate_name)
    st.write('**Lab:** IT-1042 — OfficeNet connectivity')
    a,b,c=st.columns(3)
    a.metric('Actions',len(active['history'] if active else s.history))
    b.metric('Connection outcome','Connected' if (active['connected'] if active else s.connected) else 'Not resolved')
    c.metric('Shared disruption','Yes' if (active['outage'] if active else s.outage) else 'No')
    st.markdown('### Decision timeline')
    for i,(act,out) in enumerate(zip(active['history'] if active else s.history,active['logs'] if active else s.logs),1):
        with st.expander(f'{i}. {act}',expanded=False): st.code(out, language='text')
    st.markdown('### Candidate explanation')
    st.write('**Reasoning:**',active['notes'] if active else s.notes)
    st.write('**Resolution & verification:**',active['resolution'] if active else s.resolution)
    st.write('**Adaptability:**',active['follow_answer'] if active else s.follow_answer)
    st.markdown('### AI-assisted assessment')
    report=(active['report'] if active else s.report) or {}
    st.caption(report.get('source','No review available'))
    for obs in report.get('observations',[]): st.write('• '+obs)
    st.markdown(report.get('analysis','No analysis available.'))
    with st.expander('Review rubric'):
        for r in report.get('rubric',[]): st.write('• '+r)
    st.info('MindFrame does not make hiring decisions or rank candidates. A human must review the evidence and any AI-generated analysis.')
    if s.demo_role == 'student':
        st.success('Your report is ready. To show the reviewer perspective, return to Role selection (demo only) and choose Employer / Reviewer.')
    if s.demo_role == 'student' and st.button('Start new lab',type='primary'):
        reset_lab(s.candidate_name)
        st.rerun()
