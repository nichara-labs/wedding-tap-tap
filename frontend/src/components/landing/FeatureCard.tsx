import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export const FeatureCard = ({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) => (
  <Card className="group p-6 bg-card/80 backdrop-blur-sm shadow-lg hover:shadow-xl transition-colors duration-300 items-center border border-transparent hover:border-primary/50 hover:bg-primary/10 text-center">
    <CardHeader className="p-0 flex flex-col items-center gap-3">
      <div className="p-3 rounded-full bg-primary/10 text-primary/80 group-hover:bg-primary/20 group-hover:text-primary transition-colors duration-300">
        {icon}
      </div>
      <CardTitle className="text-xl transition-colors duration-300 group-hover:text-primary">
        {title}
      </CardTitle>
    </CardHeader>
    <CardContent className="p-0 mt-2">
      <p className="text-muted-foreground">{description}</p>
    </CardContent>
  </Card>
);
