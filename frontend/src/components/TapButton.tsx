type TapType = "groom" | "bride";

interface TapButtonProps {
  type: TapType;
  onTap: (type: TapType) => void;
}

const TapButton = ({ type, onTap }: TapButtonProps) => {
  const colors = {
    groom: "from-purple-600 to-fuchsia-600",
    bride: "from-pink-500 to-fuchsia-600",
  };

  return (
    <button
      type="button"
      onClick={() => onTap(type)}
      className={`flex-1 py-8 text-2xl font-bold rounded-3xl bg-gradient-to-br ${colors[type]} shadow-2xl active:scale-95 transition`}
    >
      {type.charAt(0).toUpperCase() + type.slice(1)}
    </button>
  );
};

export default TapButton;
