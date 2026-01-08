interface PowerBarProps {
  count: number;
  baseColor: "purple" | "pink";
  label: string;
  maxCount?: number;
}

const PowerBar = ({
  count,
  baseColor,
  label,
  maxCount = 20,
}: PowerBarProps) => {
  const safeMax = Math.max(maxCount, 1);

  const getBarColor = (count: number, baseColor: string) => {
    const ratio = Math.min(count / safeMax, 1);
    if (baseColor === "purple") {
      const value = Math.floor(200 - 120 * ratio); // 200 -> 80
      return `rgb(${value}, 0, ${value + 55})`;
    } else {
      const value = Math.floor(255 - 120 * ratio); // 255 -> 135
      return `rgb(255, ${value}, ${value})`;
    }
  };

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="w-20 h-[80vh] bg-gray-700/70 rounded-3xl overflow-hidden shadow-inner flex flex-col justify-end items-center">
        <div
          className="w-full rounded-3xl transition-all duration-200 flex flex-col justify-end items-center text-white font-bold pb-2 text-3xl"
          style={{
            height: `${Math.min(count / safeMax, 1) * 100}%`,
            backgroundColor: getBarColor(count, baseColor),
          }}
        >
          {count}
        </div>
      </div>
      <div className="text-xl font-semibold tracking-wide uppercase text-white/90">
        {label}
      </div>
    </div>
  );
};

export default PowerBar;
