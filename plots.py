import matplotlib.pyplot as plt


# 1. Sessions vs Average Duration by User
def plot_sessions_vs_avg_duration(user_stats):
    """Scatter: total sessions per user vs average session duration."""
    plt.figure(figsize=(7, 5))
    plt.scatter(
        user_stats["session_count_auto"] + user_stats["session_count_manual"],
        (user_stats["mean_duration_auto"] + user_stats["mean_duration_manual"]) / 2,
        alpha=0.7
    )
    plt.xlabel("Total Sessions per User")
    plt.ylabel("Average Session Duration (s)")
    plt.title("Does Usage Frequency Affect Session Duration?")
    plt.tight_layout()
    plt.show()


def plot_session_duration_distribution(events):
    """Histogram: distribution of session durations for manual vs auto."""
    plt.figure(figsize=(8, 5))
    plt.hist(
        [events[events["type"] == "auto"]["session_duration"],
         events[events["type"] == "manual"]["session_duration"]],
        bins=50,
        label=["Auto", "Manual"],
        alpha=0.7
    )
    plt.xlabel("Session Duration (seconds)")
    plt.ylabel("Count")
    plt.title("Distribution of Session Durations by Type")
    plt.legend()
    plt.tight_layout()
    plt.show()


# 3. Session Count Summary by Type
def plot_session_count_summary(summary):
    """Bar chart: total, short, and long session counts by type."""
    summary.plot(kind="bar", figsize=(7,4))
    plt.title("Session Count Summary by Type")
    plt.ylabel("Number of Sessions")
    plt.xlabel("Type")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


# 4. Faulty Data Counts
def plot_faulty_data(processor, labels=None):
    """Bar chart: counts of faulty data types (unmatched opens, orphan closes, etc.)."""
    if labels is not None:
        processor.faulty_data.index = labels

    ax = processor.faulty_data.T.plot(kind="bar", figsize=(5,3))
    plt.title("Faulty Data Counts")
    plt.ylabel("Occurrences")
    plt.xlabel("Fault Type")
    plt.xticks(rotation=0)
    plt.legend(title="Open Type", loc="upper right")
    plt.tight_layout()
    plt.show()


# 5. Average Session Duration per User
def plot_avg_session_duration_per_user(user_stats):
    """Line chart: mean duration per user (manual vs auto)."""
    plt.plot(user_stats["user_id"], user_stats["mean_duration_auto"],
             label="Auto", marker="o")
    plt.plot(user_stats["user_id"], user_stats["mean_duration_manual"],
             label="Manual", marker="o")
    plt.title("Average Session Duration per User")
    plt.xlabel("User ID")
    plt.ylabel("Mean Duration (s)")
    plt.legend()
    plt.tight_layout()
    plt.show()


# 6. Session Count per User
def plot_session_count_per_user(user_stats):
    """Line chart: number of sessions per user (manual vs auto)."""
    plt.figure(figsize=(10, 5))
    plt.plot(user_stats["user_id"], user_stats["session_count_auto"],
             label="Auto", marker="o")
    plt.plot(user_stats["user_id"], user_stats["session_count_manual"],
             label="Manual", marker="o")
    plt.title("Session Count per User")
    plt.xlabel("User ID")
    plt.ylabel("Session Count")
    plt.legend()
    plt.tight_layout()
    plt.show()


# 7. Mean ± SD of Session Duration by Type
def plot_mean_sd_duration(mean, std_dev, cohens_d):
    """Bar chart: mean ± SD of session duration for manual vs auto, annotated with Cohen's d."""
    plt.figure(figsize=(7, 4))
    plt.bar(mean.index, mean.values,
            yerr=std_dev.values, capsize=6)
    plt.title(f"Mean ± SD of Session Duration by Type\n(Cohen's d = {cohens_d:.2f})")
    plt.ylabel("Duration (s)")
    plt.tight_layout()
    plt.show()


# 8. Boxplot of Session Duration by Type
def plot_session_duration_boxplot(events):
    """Boxplot: session duration distribution per open type."""
    flier_props = dict(marker='x', markersize=3, linestyle='none')
    events.boxplot(column="session_duration", by="type", grid=False, flierprops=flier_props)
    plt.title("Session Duration by Type")
    plt.suptitle("")
    plt.ylabel("Duration (seconds)")
    plt.tight_layout()
    plt.show()
