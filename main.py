import numpy as np
import pandas as pd
from scipy import stats
from plots import (
    plot_sessions_vs_avg_duration,
    plot_session_duration_distribution,
    plot_session_count_summary,
    plot_faulty_data,
    plot_avg_session_duration_per_user,
    plot_session_count_per_user,
    plot_mean_sd_duration,
    plot_session_duration_boxplot
)


class EventProcessor:
    def __init__(self):
        self.faulty_data = pd.DataFrame({"auto": [0, 0], "manual": [0, 0]})

    def calculate_elapsed(self, group):
        open_time = None
        open_type = None
        durations = []
        open_types = []
        for _, row in group.iterrows():
            if row['event'] == 'opened':
                if open_time is not None:
                    self.faulty_data.loc[0, row["open_type"]] += 1
                open_time = row['timestamp']
                open_type = row["open_type"]
            elif row['event'] == 'closed':
                if open_time is not None:
                    durations.append((row['timestamp'] - open_time).total_seconds())
                    open_types.append(open_type)
                    open_time = None
                else:
                    self.faulty_data.loc[1, "auto"] += 1

        if open_time is not None:
            self.faulty_data.loc[0, "auto"] += 1

        return pd.DataFrame({"type": open_types, "session_duration": durations})

    def sessions_data(self, group):
        user_sessions = len(group.index)
        avg_duration = group["duration"].mean()
        type_mode = group['open_type'].mode()

        return pd.DataFrame({"sessions": user_sessions, "duration": avg_duration, "preferred_type": type_mode})


def duration_summary(df):
    return pd.DataFrame({
        "total": df.groupby('type').size(),
        "too_short": df[df.session_duration < 8].groupby('type').size(),
        "too_long": df[df.session_duration > 11000].groupby('type').size()
    }).fillna(0).astype(int)


data = pd.read_csv('toolwindow_data.csv')
data["timestamp"] = pd.to_datetime(data["timestamp"], unit="ms")
sorted_data = data.sort_values(["user_id", "timestamp"])
processor = EventProcessor()
time_spent = sorted_data.groupby("user_id", group_keys=True).apply(processor.calculate_elapsed, include_groups=False).reset_index(level=0).reset_index(drop=True)
mean_general = time_spent.groupby("type")["session_duration"].mean()

basic_events = time_spent[(time_spent.session_duration >= 8) & (time_spent.session_duration <= 11000)]
std_dev_basic = basic_events.groupby("type")["session_duration"].std()
mean_basic = basic_events.groupby("type")["session_duration"].mean()


summary = duration_summary(time_spent)
print('Duration summary (total / too_short / too_long):')
print(summary)
print('\nStandard deviation (filtered):')
print(std_dev_basic)
print('\nMeans (filtered):')
print(mean_basic)
print('\nMeans (all):')
print(mean_general)


user_stats = time_spent.groupby(["user_id", "type"]).agg(session_count=("session_duration", "size"), mean_duration=("session_duration", "mean")).reset_index()
user_stats_pivot = user_stats.pivot(index="user_id", columns="type", values=["session_count", "mean_duration"]).fillna(0)
user_stats_pivot.columns = ['_'.join(col).strip() for col in user_stats_pivot.columns]
user_stats_pivot.reset_index(inplace=True)

manual = time_spent[time_spent["type"] == "manual"]["session_duration"].dropna()
auto = time_spent[time_spent["type"] == "auto"]["session_duration"].dropna()

t_stat, t_p = stats.ttest_ind(auto, manual, equal_var=False, nan_policy='omit')
print(f"Welch’s t-test: t={t_stat:.4f}, p-value={t_p:.4e}")
u_stat, u_p = stats.mannwhitneyu(auto, manual, alternative="two-sided")
print(f"Mann–Whitney U test: U={u_stat:.4f}, p-value={u_p:.4e}")

n1, n2 = len(auto), len(manual)
s1, s2 = auto.std(ddof=1), manual.std(ddof=1)
pooled_std = np.sqrt(((n1 - 1)*s1**2 + (n2 - 1)*s2**2) / (n1 + n2 - 2))
cohen_d = (auto.mean() - manual.mean()) / pooled_std
print(f"Cohen’s d = {cohen_d:.3f}")
print(processor.faulty_data.to_string())


plot_session_duration_distribution(basic_events)
plot_faulty_data(processor, labels=["Unmatched Opens", "Orphan Closes"])
plot_mean_sd_duration(mean_basic, std_dev_basic, cohen_d)
plot_sessions_vs_avg_duration(user_stats_pivot)
plot_session_duration_boxplot(time_spent)
plot_session_count_per_user(user_stats_pivot)
plot_avg_session_duration_per_user(user_stats_pivot)
plot_session_count_summary(summary)
