<h1>Next Availabilities!</h1>

% years = ymd_availabilities.keys()
% sorted_years = sorted(years)
% for year in sorted_years:
  % months = ymd_availabilities[year].keys()
  % sorted_months = sorted(months)
  % for month in sorted_months:
    % days = ymd_availabilities[year][month].keys()
      % sorted_days = sorted(days)
      % for day in sorted_days:
        <p>{{year}}/{{month}}/{{day}}</p>
        % for user in ymd_availabilities[year][month][day]:
          <b>{{user[1]}}</b>, <a href="/availabilities/host/{{user[0]}}">view calendar</a><br>