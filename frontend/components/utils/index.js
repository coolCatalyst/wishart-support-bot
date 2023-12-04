export function diff_time(timestamp) {
  const diff = Math.abs(new Date(Date.now()) - new Date(timestamp));
  // Conversion to various units
  let result;
  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  if (minutes == 0 && hours == 0 && days == 0) {
    if(seconds<10){
      result = 'just now'
    }else{
      result = `${seconds} seconds ago`;
    }
  } else if (minutes != 0 && hours == 0 && days == 0) {
    let minute_name = minutes == 1 ? "minute" : "minutes";
    result = `${minutes} ${minute_name} ago`;
  } else if (minutes != 0 && hours != 0 && days == 0) {
    let hour_name = hours == 1 ? "hour" : "hours";
    result = `${hours} ${hour_name} ago`;
  } else if (minutes != 0 && hours != 0 && days != 0) {
    let day_name = days == 1 ? "day" : "days";
    result = `${days} ${day_name} ago`;
  }
  return <p className="timeago">{result}</p>
}

export function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString(undefined, {
    // weekday: "long",
    day: "numeric",
    month: "numeric",
    year: "numeric",
  });
}

export const autoResize = (element) => {
  if (element.scrollHeight != 44) {
    if (element.scrollHeight == 66) {
      if (element.style.height == "66px") {
        element.style.height = "auto";
        element.style.height = element.scrollHeight + "px";
      } else {
        element.style.removeProperty("height");
      }
    } else {
      element.style.height = "auto";
      element.style.height = element.scrollHeight + "px";
    }
  }
};
