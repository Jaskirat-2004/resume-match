"""
CONFIG FOR RESUME PARSER

ALL_SKILLS    - the whitelist. Matching is now an INTERSECTION with this set, so
                anything that is not a known skill is invisible and no blacklist
                has to grow forever to keep junk out.

TOKEN RULES - important, read before adding anything.
The tokeniser splits on every character that is not a-z, 0-9, + or #. So every
entry in a skill set must be a SINGLE TOKEN made only of those characters.

    "power bi"      will NEVER match      -> put it in SKILL_PHRASES
    "node.js"       will NEVER match      -> put it in SKILL_PHRASES
    "c++"           matches fine
    "postgresql"    matches fine

Multi-word and punctuated skills go in SKILL_PHRASES, which is applied to the
raw text BEFORE splitting and collapses them into one canonical token.
"""

# ================================ SKILLS BY DOMAIN ================================
# One domain per set. To add a skill, find the right domain and add a single token.
# To add a whole new domain, define the set and add it to SKILLS_BY_DOMAIN below.

PROGRAMMING_LANGUAGES = {
    "python","java","javascript","typescript","c++","c#","go","golang","rust",
    "ruby","php","scala","kotlin","swift","perl","matlab","dart","elixir",
    "haskell","clojure","lua","groovy","assembly","fortran","cobol","vba",
    "bash","shell","powershell","sql","r","dotnet",
    # "c" is deliberately left out: too ambiguous as a bare token.
}

WEB_FRONTEND = {
    "html","html5","css","css3","sass","scss","less","tailwind","bootstrap",
    "react","reactjs","angular","angularjs","vue","vuejs","svelte","nextjs",
    "nuxt","jquery","redux","webpack","vite","babel","eslint","storybook",
    "responsive","accessibility","wcag","dom","spa","pwa","figma","webgl",
}

WEB_BACKEND = {
    "fastapi","django","flask","express","expressjs","nodejs","nestjs","spring",
    "springboot","laravel","rails","aspnet","gin","fiber","tornado","pyramid",
    "graphql","rest","restful","api","apis","grpc","soap","websocket","websockets",
    "oauth","jwt","microservices","monolith","mvc","orm","sqlalchemy","hibernate",
    "celery","rabbitmq","kafka","redis","nginx","apache","gunicorn","uvicorn",
    "pydantic","jinja","jinja2","swagger","openapi","postman",
}

DATABASES = {
    "postgresql","postgres","mysql","mariadb","sqlite","oracle","mssql",
    "sqlserver","mongodb","cassandra","dynamodb","couchdb","neo4j","redis",
    "elasticsearch","clickhouse","snowflake","bigquery","redshift","databricks",
    "duckdb","influxdb","timescaledb","cockroachdb","firestore","supabase",
    "indexing","normalization","denormalization","sharding","replication",
    "transactions","acid","olap","oltp","storedprocedures","triggers","views",
    "cte","joins","partitioning","query","optimization","schema","erd",
}

DATA_ENGINEERING = {
    "etl","elt","airflow","dagster","prefect","luigi","nifi","dbt","spark",
    "pyspark","hadoop","hive","presto","trino","flink","beam","kafka",
    "kinesis","glue","emr","datalake","datawarehouse","lakehouse","warehouse",
    "pipeline","pipelines","ingestion","batch","streaming","cdc","upsert",
    "idempotent","backfill","watermark","partition","parquet","avro","orc",
    "delta","iceberg","hudi","dataflow","orchestration","scheduler","dag","dags",
    "pandas","polars","numpy","dask",
}

DATA_ANALYTICS_BI = {
    "tableau","powerbi","looker","superset","metabase","qlik","quicksight",
    "excel","spreadsheets","pivot","vlookup","dashboards","dashboard",
    "reporting","reports","visualization","visualisation","kpi","kpis",
    "metrics","analytics","segmentation","cohort","funnel","forecasting",
    "statistics","statistical","regression","correlation","hypothesis",
    "abtesting","matplotlib","seaborn","plotly","d3","ggplot","datastudio",
}

MACHINE_LEARNING = {
    "ml","ai","machinelearning","deeplearning","nlp","llm","llms","cv",
    "tensorflow","keras","pytorch","torch","sklearn","xgboost","lightgbm",
    "catboost","huggingface","transformers","spacy","nltk","opencv",
    "classification","clustering","regression","embeddings","embedding",
    "finetuning","rag","prompt","inference","training","supervised",
    "unsupervised","reinforcement","neural","cnn","rnn","lstm","transformer",
    "bert","gpt","mlops","mlflow","kubeflow","sagemaker","vertexai","langchain",
    "vectordb","pinecone","chromadb","faiss","featureengineering",
}

DEVOPS_CLOUD = {
    "aws","azure","gcp","cloud","docker","kubernetes","k8s","helm","terraform",
    "ansible","puppet","chef","vagrant","jenkins","gitlab","githubactions",
    "circleci","travis","argocd","cicd","devops","sre","containers",
    "orchestration","serverless","lambda","ec2","s3","rds","vpc","iam",
    "cloudformation","cloudwatch","eks","ecs","fargate","route53",
    "prometheus","grafana","datadog","splunk","elk","logging","monitoring",
    "observability","alerting","autoscaling","loadbalancer","nginx",
    "linux","unix","networking","dns","ssl","tls",
}

MOBILE = {
    "android","ios","flutter","reactnative","swiftui","xamarin","ionic",
    "cordova","kotlin","swift","objectivec","gradle","xcode","playstore",
    "appstore","mobile","responsive",
}

TESTING_QA = {
    "testing","qa","pytest","unittest","junit","testng","jest","mocha","chai",
    "cypress","selenium","playwright","appium","cucumber","behave","robot",
    "tdd","bdd","unittesting","integration","regression","smoke","e2e",
    "coverage","mocking","fixtures","loadtesting","jmeter","locust","postman",
}

SECURITY = {
    "security","cybersecurity","encryption","hashing","authentication",
    "authorization","oauth","saml","sso","jwt","owasp","penetration",
    "vulnerability","firewall","ids","ips","siem","compliance","gdpr",
    "hipaa","soc2","pci","cryptography","ssl","tls","xss","csrf","sqlinjection",
}

TOOLS_PRACTICES = {
    "git","github","gitlab","bitbucket","svn","jira","confluence","trello",
    "asana","notion","slack","agile","scrum","kanban","sprint","standup",
    "retrospective","codereview","pairprogramming","documentation","uml",
    "designpatterns","solid","refactoring","debugging","profiling",
    "versioncontrol","branching","merge","rebase","pullrequest",
}

DOMAIN_BUSINESS = {
    "stakeholder","stakeholders","requirements","roadmap","backlog",
    "prioritization","estimation","budgeting","forecasting","procurement",
    "crm","erp","salesforce","sap","workflow","automation","optimization",
    "governance","audit","sla","slas",
}


SKILLS_BY_DOMAIN = {
    "Programming Languages": PROGRAMMING_LANGUAGES,
    "Web Frontend":          WEB_FRONTEND,
    "Web Backend":           WEB_BACKEND,
    "Databases":             DATABASES,
    "Data Engineering":      DATA_ENGINEERING,
    "Data Analytics & BI":   DATA_ANALYTICS_BI,
    "Machine Learning & AI": MACHINE_LEARNING,
    "DevOps & Cloud":        DEVOPS_CLOUD,
    "Mobile":                MOBILE,
    "Testing & QA":          TESTING_QA,
    "Security":              SECURITY,
    "Tools & Practices":     TOOLS_PRACTICES,
    "Business & Domain":     DOMAIN_BUSINESS,
}

# The flat vocabulary the analyzer matches against.
ALL_SKILLS = frozenset().union(*SKILLS_BY_DOMAIN.values())


# ================================ SKILL PHRASES ================================
# Multi-word or punctuated skills. Applied to the LOWERCASED text BEFORE splitting,
# so each phrase collapses into one canonical token that survives the tokeniser.
# Longest phrases are applied first, so "amazon web services" wins over "amazon".

SKILL_PHRASES = {
    "power bi":              "powerbi",
    "machine learning":      "machinelearning",
    "deep learning":         "deeplearning",
    "natural language processing": "nlp",
    "computer vision":       "cv",
    "large language model":  "llm",
    "large language models": "llms",
    "feature engineering":   "featureengineering",
    "scikit-learn":          "sklearn",
    "scikit learn":          "sklearn",
    "node.js":               "nodejs",
    "next.js":               "nextjs",
    "nest.js":               "nestjs",
    "vue.js":                "vuejs",
    "express.js":            "expressjs",
    "react.js":              "reactjs",
    "react native":          "reactnative",
    "d3.js":                 "d3",
    ".net":                  "dotnet",
    "asp.net":               "aspnet",
    "objective-c":           "objectivec",
    "spring boot":           "springboot",
    "ci/cd":                 "cicd",
    "a/b testing":           "abtesting",
    "amazon web services":   "aws",
    "google cloud platform": "gcp",
    "google cloud":          "gcp",
    "microsoft azure":       "azure",
    "github actions":        "githubactions",
    "version control":       "versioncontrol",
    "pull request":          "pullrequest",
    "code review":           "codereview",
    "pair programming":      "pairprogramming",
    "design patterns":       "designpatterns",
    "unit testing":          "unittesting",
    "load testing":          "loadtesting",
    "end-to-end":            "e2e",
    "data lake":             "datalake",
    "data warehouse":        "datawarehouse",
    "sql injection":         "sqlinjection",
    "vertex ai":             "vertexai",
    "data studio":           "datastudio",
    "stored procedures":     "storedprocedures",
    "change data capture":   "cdc",
    "single sign-on":        "sso",
    "single sign on":        "sso",
}


# ================================ SKILL ALIASES ================================
# Different spellings of the SAME skill, collapsed to one canonical token.
# Applied AFTER tokenising. Not wired into the analyzer yet - this is the
# synonym layer, and it is the next thing after the vocabulary itself.

SKILL_ALIASES = {
    "postgres":       "postgresql",
    "psql":           "postgresql",
    "pg":             "postgresql",
    "k8s":            "kubernetes",
    "golang":         "go",
    "js":             "javascript",
    "ts":             "typescript",
    "py":             "python",
    "torch":          "pytorch",
    "ml":             "machinelearning",
    "dl":             "deeplearning",
    "visualisation":  "visualization",
    "optimisation":   "optimization",
    "normalisation":  "normalization",
    "mssql":          "sqlserver",
    "reactjs":        "react",
    "vuejs":          "vue",
    "angularjs":      "angular",
    "expressjs":      "express",
    "apis":           "api",
    "dags":           "dag",
    "kpis":           "kpi",
    "llms":           "llm",
    "restful":        "rest",
    "dashboards":     "dashboard",
    "pipelines":      "pipeline",
    "containers":     "docker",
    "spreadsheets":   "excel",
}


# ================================ DISPLAY NAMES ================================
# Canonical token -> how it should be shown to a human. Anything not listed here
# is displayed with .title() or .upper() as the template prefers.

DISPLAY_NAMES = {
    "powerbi":            "Power BI",
    "machinelearning":    "Machine Learning",
    "deeplearning":       "Deep Learning",
    "nodejs":             "Node.js",
    "nextjs":             "Next.js",
    "reactnative":        "React Native",
    "dotnet":             ".NET",
    "aspnet":             "ASP.NET",
    "springboot":         "Spring Boot",
    "cicd":               "CI/CD",
    "githubactions":      "GitHub Actions",
    "abtesting":          "A/B Testing",
    "sklearn":            "scikit-learn",
    "datalake":           "Data Lake",
    "datawarehouse":      "Data Warehouse",
    "featureengineering": "Feature Engineering",
    "objectivec":         "Objective-C",
    "sqlinjection":       "SQL Injection",
    "vertexai":           "Vertex AI",
    "e2e":                "End-to-End",
    "nlp":                "NLP",
    "sql":                "SQL",
    "aws":                "AWS",
    "gcp":                "GCP",
    "api":                "API",
    "rest":               "REST",
    "etl":                "ETL",
    "elt":                "ELT",
    "kpi":                "KPI",
    "ml":                 "ML",
    "ai":                 "AI",
    "cv":                 "Computer Vision",
    "llm":                "LLM",
    "css":                "CSS",
    "html":               "HTML",
    "qa":                 "QA",
    "tdd":                "TDD",
    "bdd":                "BDD",
    "orm":                "ORM",
    "jwt":                "JWT",
    "dag":                "DAG",
    "k8s":                "Kubernetes",
    "cdc":                "CDC",
    "sso":                "SSO",
}


# ================================ ROLE PROFILES ================================
# A job role -> the domains it draws on. This powers the "what does this system
# know about for role X" page. Add a role by naming the domains it uses.

ROLE_PROFILES = {
    "Software Engineer": [
        "Programming Languages","Web Backend","Databases","Testing & QA",
        "Tools & Practices","DevOps & Cloud",
    ],
    "Backend Developer": [
        "Programming Languages","Web Backend","Databases","Testing & QA",
        "Tools & Practices",
    ],
    "Frontend Developer": [
        "Programming Languages","Web Frontend","Testing & QA","Tools & Practices",
    ],
    "Full Stack Developer": [
        "Programming Languages","Web Frontend","Web Backend","Databases",
        "Testing & QA","Tools & Practices",
    ],
    "Data Engineer": [
        "Programming Languages","Data Engineering","Databases","DevOps & Cloud",
        "Tools & Practices",
    ],
    "Data Analyst": [
        "Data Analytics & BI","Databases","Programming Languages",
        "Business & Domain",
    ],
    "Data Scientist": [
        "Programming Languages","Machine Learning & AI","Data Analytics & BI",
        "Databases",
    ],
    "ML Engineer": [
        "Programming Languages","Machine Learning & AI","DevOps & Cloud",
        "Data Engineering",
    ],
    "DevOps Engineer": [
        "DevOps & Cloud","Programming Languages","Tools & Practices","Security",
    ],
    "Cloud Engineer": [
        "DevOps & Cloud","Security","Programming Languages","Tools & Practices",
    ],
    "Mobile Developer": [
        "Mobile","Programming Languages","Testing & QA","Tools & Practices",
    ],
    "QA Engineer": [
        "Testing & QA","Programming Languages","Tools & Practices",
    ],
    "Security Engineer": [
        "Security","DevOps & Cloud","Programming Languages","Tools & Practices",
    ],
    "Database Administrator": [
        "Databases","DevOps & Cloud","Programming Languages",
    ],
    "Business Analyst": [
        "Business & Domain","Data Analytics & BI","Databases",
    ],
}

# ================================ HELPERS ================================

def skills_for_role(role: str) -> set:
    """Every skill this system knows about for a given role. Empty set if unknown."""
    skills = set()
    for domain in ROLE_PROFILES.get(role, []):
        skills |= SKILLS_BY_DOMAIN.get(domain, set())
    return skills


def display(token: str) -> str:
    """Human-readable form of a canonical skill token."""
    return DISPLAY_NAMES.get(token, token.title())
