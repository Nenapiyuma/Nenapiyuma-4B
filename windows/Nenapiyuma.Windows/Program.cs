using System.Diagnostics;
var model=args.Length>0?args[0]:"models/Nenapiyuma-4B.gguf";
var cli=args.Length>1?args[1]:"llama-cli.exe";
if(!File.Exists(model)){Console.Error.WriteLine("Missing local model: "+model);return 2;}
if(!File.Exists(cli)){Console.Error.WriteLine("Missing local llama-cli executable: "+cli);return 2;}
Console.Write("You: "); var prompt=Console.ReadLine()??"";
var psi=new ProcessStartInfo(cli){UseShellExecute=false,RedirectStandardOutput=true,RedirectStandardError=true};
psi.ArgumentList.Add("--model");psi.ArgumentList.Add(model);psi.ArgumentList.Add("--prompt");psi.ArgumentList.Add(prompt);psi.ArgumentList.Add("--n-predict");psi.ArgumentList.Add("256");
using var p=Process.Start(psi)!;Console.WriteLine(p.StandardOutput.ReadToEnd());Console.Error.WriteLine(p.StandardError.ReadToEnd());p.WaitForExit();return p.ExitCode;
