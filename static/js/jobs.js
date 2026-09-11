let allJobs = [];

document.addEventListener("DOMContentLoaded", function () {

    loadJobs();

    const searchButton = document.getElementById("searchButton");

    if (searchButton) {
        searchButton.addEventListener("click", filterJobs);
    }
});


async function loadJobs() {

    const jobsGrid = document.getElementById("jobsGrid");

    if (!jobsGrid) {
        return;
    }

    jobsGrid.innerHTML = `
        <div class="no-jobs">
            <h2>Loading jobs...</h2>
            <p>Please wait.</p>
        </div>
    `;

    try {

        const response = await fetch("/jobs");
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || "Failed to load jobs");
        }

        allJobs = Array.isArray(data) ? data : [];

        displayJobs(allJobs);

        applyUrlFilters();

    } catch (error) {

        console.error("Jobs error:", error);

        jobsGrid.innerHTML = `
            <div class="no-jobs">
                <h2>Unable to load jobs</h2>
                <p>${escapeHtml(error.message)}</p>
            </div>
        `;
    }
}


function displayJobs(jobs) {

    const jobsGrid = document.getElementById("jobsGrid");

    const countElement = document.getElementById("jobCount");

    if (countElement) {
        countElement.textContent =
            `${jobs.length} ${jobs.length === 1 ? "job" : "jobs"} found`;
    }


    if (!jobs.length) {

        jobsGrid.innerHTML = `
            <div class="no-jobs">
                <h2>No jobs found 🔍</h2>
                <p>Try changing your search or filters.</p>
            </div>
        `;

        return;
    }


    jobsGrid.innerHTML = jobs.map(function (job) {

        return `
            <div class="job-card">

                <div class="company-icon">
                    💼
                </div>

                <h3>
                    ${escapeHtml(job.title)}
                </h3>

                <div class="company">
                    ${escapeHtml(job.company)}
                </div>

                <div class="job-info">

                    <span class="job-tag">
                        📍 ${escapeHtml(job.location)}
                    </span>

                    <span class="job-tag">
                        💼 ${escapeHtml(job.job_type)}
                    </span>

                    ${
                        job.salary
                        ? `
                            <span class="job-tag">
                                💰 ${escapeHtml(job.salary)}
                            </span>
                        `
                        : ""
                    }

                </div>

                <p class="job-description">
                    ${escapeHtml(job.description)}
                </p>

                <div class="job-actions">

                    <a
                        href="/job-details-page?id=${job.id}"
                        class="details-btn">
                        View Details
                    </a>

                    <a
                        href="/job-details-page?id=${job.id}"
                        class="apply-btn">
                        Apply →
                    </a>

                </div>

            </div>
        `;

    }).join("");
}


function filterJobs() {

    const search =
        document.getElementById("searchInput").value
            .trim()
            .toLowerCase();

    const location =
        document.getElementById("locationInput").value
            .trim()
            .toLowerCase();

    const jobType =
        document.getElementById("jobType").value;


    const filtered = allJobs.filter(function (job) {

        const title =
            String(job.title || "").toLowerCase();

        const company =
            String(job.company || "").toLowerCase();

        const jobLocation =
            String(job.location || "").toLowerCase();

        const type =
            String(job.job_type || "");


        const matchesSearch =
            !search ||
            title.includes(search) ||
            company.includes(search);

        const matchesLocation =
            !location ||
            jobLocation.includes(location);

        const matchesType =
            !jobType ||
            type === jobType;


        return (
            matchesSearch &&
            matchesLocation &&
            matchesType
        );
    });


    displayJobs(filtered);
}


function applyUrlFilters() {

    const params =
        new URLSearchParams(window.location.search);

    const search = params.get("search");
    const location = params.get("location");
    const category = params.get("category");


    if (search) {
        document.getElementById("searchInput").value = search;
    }

    if (location) {
        document.getElementById("locationInput").value = location;
    }


    if (!search && !location && !category) {
        return;
    }


    let filtered = allJobs;


    if (search) {

        const query = search.toLowerCase();

        filtered = filtered.filter(function (job) {

            const text = `
                ${job.title || ""}
                ${job.company || ""}
                ${job.description || ""}
                ${job.requirements || ""}
            `.toLowerCase();

            return text.includes(query);
        });
    }


    if (location) {

        const place = location.toLowerCase();

        filtered = filtered.filter(function (job) {

            return String(job.location || "")
                .toLowerCase()
                .includes(place);
        });
    }


    if (category) {

        const categoryKeywords = {

            Software: [
                "software",
                "developer",
                "development",
                "programmer",
                "python",
                "java",
                "web"
            ],

            AI: [
                "ai",
                "machine learning",
                "ml",
                "artificial intelligence"
            ],

            Data: [
                "data",
                "analytics",
                "analyst",
                "scientist"
            ],

            Design: [
                "design",
                "designer",
                "ui",
                "ux",
                "creative"
            ]
        };


        const keywords =
            categoryKeywords[category] || [];


        if (keywords.length) {

            filtered = filtered.filter(function (job) {

                const text = `
                    ${job.title || ""}
                    ${job.company || ""}
                    ${job.description || ""}
                    ${job.requirements || ""}
                `.toLowerCase();

                return keywords.some(function (keyword) {
                    return text.includes(keyword);
                });
            });
        }
    }


    displayJobs(filtered);
}


function clearFilters() {

    document.getElementById("searchInput").value = "";
    document.getElementById("locationInput").value = "";
    document.getElementById("jobType").value = "";

    window.history.replaceState(
        {},
        "",
        "/jobs-page"
    );

    displayJobs(allJobs);
}


function escapeHtml(value) {

    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}