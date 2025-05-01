import { EliminationReasonEnum, RoleEnum, StatusEnum } from '@/custom_types/enums.ts';

export interface Player {
  id: number;
  nickname: string;
  fouls: number;
  role: typeof RoleEnum;
  status: typeof StatusEnum;
  elimination_reason: typeof EliminationReasonEnum;
  show_role: boolean;
}
