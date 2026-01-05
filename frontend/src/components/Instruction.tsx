interface InstructionProps {
  visible: boolean;
}

const Instruction = ({ visible }: InstructionProps) => {
  if (!visible) return null;
  return (
    <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 text-3xl font-bold text-white z-20">
      Tap, match and open
    </div>
  );
};

export default Instruction;
