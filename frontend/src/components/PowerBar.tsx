interface PowerBarProps {
  count: number;
  baseColor: "purple" | "pink";
  label: string;
}

const PowerBar = ({ count, baseColor, label }: PowerBarProps) => {
  const MAX_COUNT = 20; // match the main constant

  const getBarColor = (count: number, baseColor: string) => {
    const ratio = Math.min(count / MAX_COUNT, 1);
    if (baseColor === "purple") {
      const value = Math.floor(200 - 120 * ratio); // 200 -> 80
      return `rgb(${value}, 0, ${value + 55})`;
    } else {
      const value = Math.floor(255 - 120 * ratio); // 255 -> 135
      return `rgb(255, ${value}, ${value})`;
    }
  };

  return (
    <div className="w-20 h-[80vh] bg-gray-700 rounded-3xl overflow-hidden shadow-inner flex flex-col justify-end items-center">
      <div
        className="w-full rounded-3xl transition-all duration-200 flex flex-col justify-end items-center text-white font-bold pb-2 text-3xl"
        style={{
          height: `${(count / MAX_COUNT) * 100}%`,
          backgroundColor: getBarColor(count, baseColor),
        }}
      >
        {count}
      </div>
    </div>
  );
};

export default PowerBar;
